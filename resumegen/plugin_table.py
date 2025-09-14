# Idea: specify column and row count (and in the future their widths/heights?), then give a list of Cells expressed as Cell(contents, n_col=1, n_row=1).
# This can then be resolved into whatever combination of multirow/multicol the backend needs

# need to think about how to express row/col lines


from dataclasses import dataclass
import dataclasses
from enum import IntEnum
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
)
import pandas as pd
from turnip_text import (
    Block,
    BlockScope,
    BlockScopeBuilder,
    CoercibleToInline,
    Header,
    Inline,
    InlineScope,
    Paragraph,
    InlineScopeBuilder,
    Raw,
    coerce_to_inline,
)
from turnip_text.build_system import BuildSystem
from turnip_text.doc.anchors import Anchor
from turnip_text.doc.user_nodes import UserNode
from turnip_text.env_plugins import DocEnv, EnvPlugin, FmtEnv, in_doc
from turnip_text.helpers import block_scope_builder
from turnip_text.render.latex.backrefs import LatexBackrefMethod
from turnip_text.render.latex.counter_resolver import LatexCounterDecl
from turnip_text.render.latex.renderer import LatexCounterFormat, LatexCounterStyle, LatexRenderer
from turnip_text.render.latex.setup import LatexPlugin, LatexSetup
from turnip_text.render.manual_numbering import SimpleCounterFormat, SimpleCounterStyle
from turnip_text.render.markdown.renderer import MarkdownCounterFormat, MarkdownPlugin, MarkdownRenderer, MarkdownSetup




class Align:
    pass


class BasicAlign(Align, IntEnum):
    Start = (0,)
    Middle = (1,)
    End = 2

# For compatibility
Align.Start = BasicAlign.Start # type: ignore
Align.Middle = BasicAlign.Middle # type: ignore
Align.End = BasicAlign.End # type: ignore

@dataclass(frozen=True)
class FixedWidthAlign(Align):
    text: BasicAlign
    width: str # e.g. "2cm" TODO make an actual measurement system


class HRuleType(IntEnum):
    Top = (0,)
    Middle = (1,)
    Bottom = 2


@dataclass
class Cell:
    contents: Inline
    h_size: int = 1
    v_size: int = 1
    h_align: Optional[BasicAlign] = None
    v_align: Optional[BasicAlign] = None  # Only used in multirow cells (v_size > 1)

    def __init__(
        self,
        contents: CoercibleToInline,
        h_size: int = 1,
        v_size: int = 1,
        h_align: BasicAlign | None = None,
        v_align: BasicAlign | None = None,
    ):
        self.contents = coerce_to_inline(contents)
        self.h_size = h_size
        self.h_align = h_align
        self.v_size = v_size
        self.v_align = v_align


@dataclass(frozen=True)
class Table(UserNode, Block, BlockScopeBuilder):
    anchor: Anchor

    n_rows: int  # Number of rows. We can't specify vertical align right now
    cols: List[Align]  # List of h-align

    cells: List[Tuple[Cell, int, int]]  # (cell, top_left_row, top_left_col) sorted by (top_left_row, top_left_col)
    cell_occupancy: List[List[int]]

    # TODO this cannot express LaTeX \cline - lines below specific cells
    hrules: Mapping[
        int, HRuleType
    ]  # List of row indices to put bars on the *top*. i.e. if (0, HRuleType.<some type>) is in hrules there is a rule at the top of the table.
    vrules: List[
        int
    ]  # List of column indices to put bars on the *left*. i.e. if 0 is in vrule then the left side of the first column gets a rule

    placement: Optional[str] = None
    caption: Optional[Block] = None

    def child_nodes(self) -> Iterable[Block | Inline] | None:
        return [cell.contents for (cell, x, y) in self.cells] + [self.caption] if self.caption else []

    def build_from_blocks(self, bs: BlockScope) -> Block | None:
        assert self.caption is None
        return dataclasses.replace(self, caption=bs)


# Used inside a [table] block. Doesn't render
@dataclass(frozen=True)
class InlineCell(Inline):
    cell: Cell


# Used inside a [table] block.
@dataclass(frozen=True)
class InlineCellBuilder(InlineScopeBuilder):
    h_size: int = 1
    v_size: int = 1
    h_align: Optional[BasicAlign] = None
    v_align: Optional[BasicAlign] = None

    def __call__(self, **kwargs: Any) -> Any:
        return dataclasses.replace(self, **kwargs)

    def build_from_inlines(self, inls: InlineScope) -> Inline:
        return InlineCell(
            Cell(
                contents=inls,
                h_size=self.h_size,
                h_align=self.h_align,
                v_size=self.v_size,
                v_align=self.v_align,
            )
        )


TRow = TypeVar("TRow", bound=tuple)


TABLE_LABEL_KIND = "table"


class TablePlugin(EnvPlugin):
    def _doc_nodes(self) -> Sequence[type[Block] | type[Inline] | type[Header]]:
        return [Table]
    
    def _countables(self) -> Sequence[str]:
        return (TABLE_LABEL_KIND,)

    # TODO accept Sequence[Union[Cell, CoercibleToInline]]
    # and make Cell accept CoercibleToInline
    @in_doc
    def table_from_cells(
        self,
        doc: DocEnv,
        label: str,
        cols: Union[int, List[Align]],
        n_rows: int,
        cells: List[Cell],
        hrules: Mapping[int, HRuleType] | List[int] | None = None,
        includes_header: bool = True,
        vrules: List[int] | None = None,
        placement: Optional[str] = None,
    ) -> Table:
        if isinstance(cols, int):
            cols = [BasicAlign.Middle] * cols

        # Check Cells by computing a cell_occupancy table
        # TODO would it be useful to provide an extra list associating each cell with it's top-left?

        cell_occupancy = []  # indexed row, column
        for _ in range(n_rows):
            cell_occupancy.append([-1] * len(cols))

        cells_with_points = []

        cursor = [0, 0]  # row, column
        for cell_idx, cell in enumerate(cells):
            if not isinstance(cell, Cell):
                raise ValueError(f"Passed {cell} into table_from_cells which isn't a Cell instance")

            if cell.h_size < 1 or cell.v_size < 1:
                raise RuntimeError(f"Cell {cell} has invalid sizes")

            cells_with_points.append((cell, cursor[0], cursor[1]))

            for i in range(cursor[0], cursor[0] + cell.v_size):
                for j in range(cursor[1], cursor[1] + cell.h_size):
                    if i >= n_rows or j >= len(cols):
                        raise RuntimeError(
                            f"Cell {cell_idx} exceeds the bounds of the table"
                        )
                    if cell_occupancy[i][j] != -1:
                        raise RuntimeError(
                            f"Cell {cell_idx} and cell {cell_occupancy[i][j]} overlap!"
                        )
                    cell_occupancy[i][j] = cell_idx

            cursor[1] += cell.h_size

            # If this cell pushed us to the end of the line, wrap around
            if cursor[1] == len(
                cols
            ):  # if it were >, then at some point i would have been == len(cols) in the loop and the RuntimeError would already have happened
                cursor = [cursor[0] + 1, 0]
                if cursor[0] >= n_rows:
                    break
            # If we're now looking at an occupied cell, continue through the cells until we hit one that's outside.
            # The whole row may be taken up (imagine a three-high full-width cell) so we may need to go down a row again until we get there.
            while cell_occupancy[cursor[0]][cursor[1]] != -1:
                cursor[1] += 1
                if cursor[1] >= len(cols):
                    cursor = [cursor[0] + 1, 0]
                    if cursor[0] >= n_rows:
                        break

        if any(cell_idx == -1 for col in cell_occupancy for cell_idx in col):
            raise RuntimeError(
                f"data for table '{label}' doesn't fully fill out the cells: expected {n_rows} rows, {len(cols)} columns"
            )

        if hrules is None:
            if includes_header:
                hrules = {
                    0: HRuleType.Top,
                    1: HRuleType.Middle,
                    n_rows: HRuleType.Bottom,
                }
            else:
                hrules = {0: HRuleType.Top, n_rows: HRuleType.Bottom}
        elif isinstance(hrules, list):
            hrules = {
                i: HRuleType.Top
                if i == 0
                else (HRuleType.Bottom if i == n_rows else HRuleType.Middle)
                for i in hrules
            }

        if vrules is None:
            vrules = []

        t = Table(
            anchor=doc.anchors.register_new_anchor(TABLE_LABEL_KIND, id=label),
            n_rows=n_rows,
            cols=cols,
            cells=cells_with_points,
            cell_occupancy=cell_occupancy,
            hrules=hrules,
            vrules=vrules,
            placement=placement,
        )
        return t

    def table_from_pandas(
        self, label: str, df: pd.DataFrame, placement: Optional[str] = None
    ) -> Table:
        return self.table_from_data(
            label,
            [tuple(df.columns.values)]
            + [row for row in df.itertuples(index=False, name=None)],
            has_header=True,
            placement=placement,
        )

    # TODO more table_from_x
    def table_from_data(
        self,
        label: str,
        data: Sequence[TRow],
        has_header: bool = True,
        placement: Optional[str] = None,
    ) -> Table:
        hrules = {0: HRuleType.Top, len(data): HRuleType.Bottom}
        if has_header:
            hrules[1] = HRuleType.Middle

        return self.table_from_cells(
            label,
            cols=len(data[0]),
            n_rows=len(data),
            cells=[
                Cell(c) if not isinstance(c, Cell) else c for row in data for c in row
            ],
            hrules=hrules,
            vrules=None,
            placement=placement,
        )

    def table(
        self,
        label: str,
        cols: Union[int, List[Align]],
        n_rows: int,
        hrules: Mapping[int, HRuleType] | List[int] | None = None,
        includes_header: bool = True,
        vrules: List[int] | None = None,
        placement: Optional[str] = None,
    ) -> BlockScopeBuilder:
        @block_scope_builder
        def table_builder(blocks: BlockScope) -> Table:
            cells = []
            # TODO need DFS to support things other than paragraphs here
            for block in blocks:
                assert isinstance(block, Paragraph)
                for sentence in block:
                    for inl in sentence:
                        assert isinstance(inl, InlineCell)
                        cells.append(inl.cell)

            return self.table_from_cells(
                label,
                n_rows=n_rows,
                cols=cols,
                hrules=hrules,
                includes_header=includes_header,
                vrules=vrules,
                cells=cells,
                placement=placement,
            )

        return table_builder

    cell = InlineCellBuilder()

    # Expose the types to the document context

    def _interface(self) -> Dict[str, Any]:
        return {
            "table_from_cells": self.table_from_cells,
            "table_from_pandas": self.table_from_pandas,
            "table_from_data": self.table_from_data,
            "table": self.table,
            "cell": self.cell,
            "Align": Align,
            "BasicAlign": BasicAlign,
            "FixedWidthAlign": FixedWidthAlign,
            "HRuleType": HRuleType,
            "Cell": Cell,
        }


# THIS NEEDS TESTING
# TODO could make a verion of this with nicematrix? Requires tikz tho
# https://tex.stackexchange.com/a/567702
class LatexTablePlugin(LatexPlugin, TablePlugin):
    def _register(self, build_sys: BuildSystem, setup: LatexSetup) -> None:
        super()._register(build_sys, setup)

        setup.package_resolver.request_latex_package(
            "booktabs", reason="tables generated by the table plugin"
        )
        setup.package_resolver.request_latex_package(

            "multirow", reason="tables generated by the table plugin"
        )
        setup.emitter.register_block_or_inline(Table, self._emit_table)
        setup.counter_resolver.declare_latex_counter("table", LatexCounterDecl(
            provided_by_docclass_or_package=True,
            default_reset_latex_counter=None,
            default_fmt=LatexCounterFormat(
                name="table",
                style=LatexCounterStyle.Arabic,
            ),
        ),
        backref_method=(LatexBackrefMethod.Cleveref, LatexBackrefMethod.Hyperlink, LatexBackrefMethod.ManualRef)
        )
        setup.counter_resolver.declare_tt_counter("table", "table")

    def _emit_table(
        self,
        t: Table,
        renderer: LatexRenderer,
        fmt: FmtEnv,
    ) -> None:
        ALIGN_TO_VPOS = {
            BasicAlign.Start: "t",
            BasicAlign.Middle: "c",
            BasicAlign.End: "b",
        }
        HRULE_TO_LATEX = {
            HRuleType.Top: "\\toprule",
            HRuleType.Middle: "\\midrule",
            HRuleType.Bottom: "\\bottomrule",
        }

        def align_to_colspec(align: Align) -> str:
            if align == BasicAlign.Start:
                return "l"
            elif align == BasicAlign.Middle:
                return "c"
            elif align == BasicAlign.End:
                return "r"
            elif isinstance(align, FixedWidthAlign):
                assert "LaTeX p{} type is left-aligned" and (align.text == BasicAlign.Start)
                return f"p{{{align.width}}}"
            else:
                raise ValueError(f"Can't translate {align} to colspec")

        LINE_SPLIT = "\\\\"

        # Generate the column spec
        column_spec = ""
        for i, align in enumerate(t.cols):
            if i in t.vrules:
                column_spec += "|"
            column_spec += align_to_colspec(align)
        if len(t.cols) in t.vrules:
            column_spec += "|"

        # TODO we really need a better way to do environments with arguments
        renderer.emit_macro("begin")
        renderer.emit_braced(Raw("table"))
        if t.placement:
            renderer.emit_sqr_bracketed(Raw(t.placement))
        else:
            renderer.emit_sqr_bracketed(Raw("h!"))
        renderer.emit_newline()

        with renderer.indent(4):
            renderer.emit_macro("centering")
            renderer.emit_newline()

            renderer.emit_macro("begin")
            renderer.emit_braced(Raw("tabular"))
            renderer.emit_braced(Raw(column_spec))
            renderer.emit_newline()

            with renderer.indent(4):
                last_cell_emitted = -1
                for row_idx in range(t.n_rows):
                    # If this isn't the first row, put in a line split to finish the previous line.
                    # We do this here, because we don't want to do it at the end of the final row
                    if row_idx > 0:
                        renderer.emit_raw(LINE_SPLIT)
                        renderer.emit_newline()

                    # If we're supposed to emit a horizontal rule... do that
                    if row_idx in t.hrules:
                        renderer.emit_raw(HRULE_TO_LATEX[t.hrules[row_idx]])
                        renderer.emit_newline()

                    col_idx = 0
                    while col_idx < len(t.cols):
                        cell_idx = t.cell_occupancy[row_idx][col_idx]
                        cell, top_left_row, top_left_col = t.cells[cell_idx]

                        # If this isn't the first column, put a cell separator to finish the previous cell.
                        # We do this here, because we don't want to do it at the end of the final cell
                        if col_idx > 0:
                            renderer.emit_raw(" & ")

                        if cell_idx > last_cell_emitted:
                            # Encountered a new cell - this must be the top left of the cell, let's emit it

                            # The correct order seems to be \multicolumn { \multirow { contents } }

                            if cell.h_size != 1:
                                renderer.emit_macro("multicolumn")
                                # First non-optional arg: size
                                renderer.emit_braced(
                                    Raw(str(cell.h_size))
                                )
                                # Second non-optional arg: column spec
                                colspec = align_to_colspec(
                                    cell.h_align
                                    if cell.h_align is not None
                                    else t.cols[col_idx]
                                )
                                if col_idx in t.vrules:
                                    colspec = "|" + colspec
                                if col_idx + cell.h_size in t.vrules:
                                    colspec = colspec + "|"
                                renderer.emit_braced(Raw(colspec))
                                # Third non-optional arg: the contents!
                                # Open a brace, we'll close it later
                                renderer.emit_raw("{")

                            if cell.v_size != 1:
                                renderer.emit_macro("multirow")
                                # Optional arg: v-align
                                # The default v-align is Middle
                                if (
                                    cell.v_align is not None
                                    and cell.v_align != BasicAlign.Middle
                                ):
                                    renderer.emit_sqr_bracketed(
                                        Raw(f"{ALIGN_TO_VPOS[cell.v_align]}")
                                    )
                                # First non-optional arg: size
                                renderer.emit_braced(Raw(str(cell.v_size)))
                                # Second non-optional arg: width text is kept to inside the cell.
                                # * -> natural text width
                                # = -> fit to the original width of this column
                                renderer.emit_braced(Raw("*"))
                                # Third non-optional arg: the contents!
                                # Open a brace, we'll close it later
                                renderer.emit_raw("{")

                            # TODO handle cell.v_align when it's not in a multirow?

                            renderer.emit_inline(cell.contents)

                            # Close the multirow, if we opened it
                            if cell.v_size != 1:
                                renderer.emit_raw("}")

                            # Close the multicolumn, if we opened it
                            if cell.h_size != 1:
                                renderer.emit_raw("}")

                            # We've now emitted the cell!
                            last_cell_emitted = cell_idx

                            # We need to step the col_idx forward by h_size, not 1, because \multicolumn{} consumes cells
                            col_idx += cell.h_size
                        else:
                            # This part of the table is already occupied by a cell we emitted long ago.
                            # Normally, just emit nothing.
                            # If this long-ago cell was a multirow and multicolumn, and we are at the same column but different row to when it started, we need to do an empty multicolumn to fill out the whitespace (https://tex.stackexchange.com/q/167366)
                            if cell.h_size > 1 and col_idx == top_left_col:
                                renderer.emit_macro("multicolumn")
                                # First non-optional arg: size
                                renderer.emit_braced(Raw(str(cell.h_size)))
                                # Second non-optional arg: column spec
                                colspec = align_to_colspec(
                                    cell.h_align
                                    if cell.h_align is not None
                                    else t.cols[col_idx]
                                )
                                if col_idx in t.vrules:
                                    colspec = "|" + colspec
                                if col_idx + cell.h_size in t.vrules:
                                    colspec = colspec + "|"
                                renderer.emit_braced(Raw(colspec))
                                # Third non-optional arg: the contents, which are nil
                                renderer.emit_raw("{}")
                                # We need to step the col_idx forward by h_size, not 1, because \multicolumn{} consumes cells
                                col_idx += cell.h_size
                            else:
                                col_idx += 1

                # Check for the closing hrule
                if t.n_rows in t.hrules:
                    renderer.emit_raw(LINE_SPLIT)
                    renderer.emit_newline()
                    renderer.emit_raw(HRULE_TO_LATEX[t.hrules[t.n_rows]])

            renderer.emit_newline()
            renderer.emit_macro("end")
            renderer.emit_braced(Raw("tabular"))
            renderer.emit_newline()

            if t.caption is not None:
                renderer.emit_macro("caption")
                renderer.emit_braced(t.caption)
                renderer.emit_newline()

            renderer.emit_anchor(t.anchor)
            renderer.emit_newline()

        renderer.emit_macro("end")
        renderer.emit_braced(Raw("table"))


class MarkdownTablePlugin(MarkdownPlugin, TablePlugin):
    def _register(self, build_sys: BuildSystem, setup: MarkdownSetup) -> None:
        super()._register(build_sys, setup)
        setup.emitter.register_block_or_inline(Table, self._emit_table)
        setup.define_counter_rendering("table", MarkdownCounterFormat("Table", SimpleCounterStyle.Arabic))

    def _emit_table(
        self,
        t: Table,
        renderer: MarkdownRenderer,
        fmt: FmtEnv,
    ) -> None:
        # TODO borders, alignment

        with renderer.html_mode():
            with renderer.emit_tag("figure", indent=4):
                with renderer.emit_tag(
                    "table", 'style="table-layout: fixed; width=400px"', indent=4
                ):
                    renderer.emit_anchor(t.anchor)
                    renderer.emit_newline()

                    last_cell_emitted = -1
                    for row_idx in range(t.n_rows):
                        if row_idx != 0:
                            # a newline between each tr
                            renderer.emit_newline()

                        with renderer.emit_tag("tr", indent=4):
                            col_idx = 0
                            first_elem_of_row = True
                            while col_idx < len(t.cols):
                                cell_idx = t.cell_occupancy[row_idx][col_idx]
                                cell, top_left_row, top_left_col = t.cells[cell_idx]

                                if cell_idx > last_cell_emitted:
                                    # It's a new cell, emit it
                                    if not first_elem_of_row:
                                        renderer.emit_newline()
                                    first_elem_of_row = False

                                    if cell.h_size != 1 or cell.v_size != 1:
                                        props = f'colspan="{cell.h_size}" rowspan="{cell.v_size}"'
                                    else:
                                        props = ""
                                    with renderer.emit_tag("td", props):
                                        renderer.emit_inline(cell.contents)
                                    last_cell_emitted = cell_idx
                                col_idx += cell.h_size

                renderer.emit_newline()
                if t.caption is not None:
                    with renderer.emit_tag("figcaption"):
                        renderer.emit_block(t.caption)

from turnip_text.render.pandoc import PandocPlugin, PandocRenderer, PandocSetup, pan

class PandocTablePlugin(PandocPlugin, TablePlugin):
    def _register(self, build_sys: BuildSystem, setup: PandocSetup) -> None:
        super()._register(build_sys, setup)
        setup.makers.register_block(Table, self._build_table)
        setup.define_renderable_counter("table", SimpleCounterFormat("Table", SimpleCounterStyle.Arabic))

    def _build_table(self, table: Table, p: PandocRenderer, fmt: FmtEnv) -> pan.Block:
        rows: List[List[pan.Cell]] = []
        curr_row: Optional[List[pan.Cell]] = None
        curr_y: Optional[int] = None

        pan_h_align = {
            BasicAlign.Start: pan.AlignLeft(),
            BasicAlign.Middle: pan.AlignCenter(),
            BasicAlign.End: pan.AlignRight(),
            None: pan.AlignDefault(),
        }

        for (cell, x, y) in table.cells:
            if curr_y == None:
                assert y == 0
                curr_row = []
                curr_y = 0
            else:
                assert curr_row is not None
                # Advance curr_y until it's the same as the cell y.
                # This can take multiple hits if, for whatever reason, a Table row is filled with multicolumn cells and has none of its own.
                while curr_y != y:
                    rows.append(curr_row)
                    curr_row = []
                    curr_y += 1
            curr_row.append(pan.Cell(
                ("", [], []),
                pan_h_align[cell.h_align],
                pan.RowSpan(cell.v_size),
                pan.ColSpan(cell.h_size),
                [pan.Para([p.make_inline(cell.contents)])]
            ))

        # The pandoc table structure is (TableHead, TableBody, TableFoot)
        # TableHead = (Attr, [Row])
        # TableBody = (Attr, RowHeadColumns(int), [Row], [Row])
        # TableFoot = (Attr, [Row])
        # My understanding is that you can have multiple rows in the TableHead, followed by a header rule,
        # then for each TableBody:
        #     if the first List[Row] is not empty, a set of rows and a plain horizontal rule, else nothing
        #         note that those Rows can be made header-y by setting RowHeadColumns to non-zero(?)
        #     then the other [Row]s.
        # then if the TableFoot [Row] is not empty, a footer rule and the rest of the rows.

        # We can't guarantee the correct HRuleType everywhere but we can otherwise translate this reliably.
        # First, we can deal with the foot: if the last HRule is a Bottom, take all rows after that point and put then in a TableFoot.
        # Otherwise, use an empty TableFoot.
        # TableHead is a little different... kinda.
        
        # TODO RETHINK THIS. LaTeX tables typically have the HRule.Bottom after everything, and HRule.Top before everything

        hrules_to_process = list(table.hrules.keys())
        head_rows = []
        foot_rows = []
        # Process footer first, because we're mutating the `rows` list and want the indices to be consistent.
        last_rule_idx = max(hrules_to_process)
        if table.hrules[last_rule_idx] == HRuleType.Bottom:
            foot_rows = rows[last_rule_idx:]
            rows = rows[:last_rule_idx]
            # we have processed the last hrule
            hrules_to_process.remove(last_rule_idx)
        first_rule_idx = min(table.hrules.keys())
        if table.hrules[first_rule_idx] == HRuleType.Top:
            head_rows = rows[:first_rule_idx]
            rows = rows[first_rule_idx:]
            # we have processed the first hrule
            hrules_to_process.remove(first_rule_idx)
            # to keep hrules_to_process indices in the same domain as the `rows` list, which just had `first_rule_idx+1` items removed, subtract `first_rule_idx+1` from each hrule_to_process
            hrules
        

        pan.TableBody()

        return pan.Table()
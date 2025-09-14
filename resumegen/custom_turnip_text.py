from dataclasses import dataclass
import json
from typing import Any, Dict
from turnip_text import CoercibleToInline, Inline
from turnip_text.cli import GeneratedSetup, TurnipTextSetup
from turnip_text.plugins.cites.latex import LatexBiblatexCitationPlugin
from turnip_text.plugins.cites.markdown import MarkdownCiteProcCitationPlugin
from turnip_text.plugins.doc_structure.markdown import MarkdownStructurePlugin
from turnip_text.plugins.footnote.latex import LatexFootnotePlugin
from turnip_text.plugins.footnote.markdown import MarkdownFootnotePlugin_AtEnd
from turnip_text.plugins.inline_fmt.latex import LatexInlineFormatPlugin
from turnip_text.plugins.inline_fmt.markdown import MarkdownInlineFormatPlugin
from turnip_text.plugins.list.latex import LatexListPlugin
from turnip_text.plugins.list.markdown import MarkdownListPlugin
from turnip_text.plugins.primitives.latex import LatexPrimitivesPlugin
from turnip_text.plugins.primitives.markdown import MarkdownPrimitivesPlugin
from turnip_text.plugins.url.latex import LatexUrlPlugin
from turnip_text.plugins.url.markdown import MarkdownUrlPlugin
from turnip_text.env_plugins import EnvPlugin
from turnip_text.render.latex.renderer import LatexRenderer
from turnip_text.render.latex.setup import LatexPlugin
from turnip_text.render import RenderPlugin, RenderSetup
from turnip_text.render.latex.setup import LatexSetup
from turnip_text.render.markdown.renderer import HtmlSetup, MarkdownPlugin, MarkdownSetup
from turnip_text.render.pandoc import PandocPlugin, PandocSetup
from turnip_text.plugins.cites.pandoc import PandocCitationPlugin
from turnip_text.plugins.doc_structure.pandoc import PandocStructurePlugin

from turnip_text.plugins.inline_fmt.pandoc import PandocInlineFormatPlugin
from turnip_text.plugins.list.pandoc import PandocListPlugin
from turnip_text.plugins.primitives.pandoc import PandocPrimitivesPlugin
from turnip_text.plugins.url.pandoc import PandocUrlPlugin

from plugin_table import LatexTablePlugin, MarkdownTablePlugin

class CvPlugin(EnvPlugin):
    resume_json_object: Dict[str, Any]

    def __init__(self, resume_json_object):
        self.resume_json_object = resume_json_object
    
    # def name(self, name: CoercibleToInline) -> Inline:
    #     pass

    # def 

class LatexCvPlugin(CvPlugin, LatexPlugin):
    def _register(self, build_sys, setup):
        setup.require_document_class("article")

class MarkdownCvPlugin(CvPlugin, MarkdownPlugin):
    def _register(self, build_sys, setup):
        pass

class PandocCvPlugin(CvPlugin, PandocPlugin):
    def _register(self, build_sys, setup):
        pass

class CvSetup(TurnipTextSetup):
    def generate_setup(self, input_stem: str, requested_format: str, resumejson: str="", **kwargs: str) -> GeneratedSetup:
        if not resumejson:
            raise RuntimeError("Specify a resume.json file to load with --setuparg 'resumejson:<path>'")
        with open(resumejson, "r", encoding="utf8") as f:
            resume_json_object = json.load(f)

        if requested_format == "latex":
            return GeneratedSetup(
                LatexSetup(
                    default_font_packages=False,
                ),
                [
                    LatexCvPlugin(resume_json_object),
                    LatexListPlugin(indent_list_items=True),
                    LatexInlineFormatPlugin(),
                    LatexUrlPlugin(),
                    LatexPrimitivesPlugin(),
                    LatexTablePlugin(),
                ],
                f"{input_stem}.tex"
            )
        elif requested_format == "markdown":
            return GeneratedSetup(
                MarkdownSetup(),
                [
                    MarkdownCvPlugin(resume_json_object),
                    MarkdownListPlugin(indent_list_items=True),
                    MarkdownInlineFormatPlugin(),
                    MarkdownUrlPlugin(),
                    MarkdownPrimitivesPlugin(),
                    MarkdownTablePlugin(),
                ],
                f"{input_stem}.md"
            )
        elif requested_format == "docx":
            return GeneratedSetup(
                PandocSetup("docx"),
                [
                    PandocCvPlugin(resume_json_object),
                    PandocListPlugin(),
                    PandocInlineFormatPlugin(),
                    PandocUrlPlugin(),
                    PandocPrimitivesPlugin(),
                    PandocTablePlugin(),
                ],
                f"{input_stem}.docx"
            )

        return super().generate_setup(input_stem, requested_format, **kwargs)
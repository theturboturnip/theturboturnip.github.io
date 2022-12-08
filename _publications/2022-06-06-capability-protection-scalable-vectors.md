---
title: "Capability-Based Memory Protection for Scalable Vector Processing"
collection: publications
permalink: /academia/2022-06-06-capability-protection-scalable-vectors
redirect_from:
    - /publication/2022-06-06-capability-protection-scalable-vectors
    - /publication/2022-06-06-capability-protection-scalable-vectors.html
    - /cheri-rvv
    - /cheri-rvv/
header:
    teaser: "2022-06-06-capability-protection-header-small.png"
excerpt: "On applying CHERI-based memory protection to vector processors, particularly scalable vector models e.g. Arm SVE and RISC-V &quot;V&quot;."
date: 2022-06-06
paperurl: 'https://theturboturnip.github.io/files/2022-06-06-capability-protection-scalable-vectors.pdf'
citation: 'Stark, S. (2022). Capability-Based Memory Protection for Scalable Vector Processing. [MPhil thesis]. University of Cambridge.'
course: 'Advanced Computer Science MPhil @ University of Cambridge'
---

<img src='/images/2022-06-06-capability-protection-header-small.png'><br/>

[**Winner of the RISE 2022 Student Competition!**](/posts/2022/12/cheri-rvv-rise)

My master's project examines the impact of combining [CHERI](https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/)'s hardware memory protection with vector processing, particularly vectorized loads and stores, by designing a potential specification for "CHERI-RVV" - a CHERI version of [the RISC-V "V" scalable vector extension](https://github.com/riscv/riscv-v-spec).

<iframe src="https://www.youtube-nocookie.com/embed/J82OFvF3yGY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Artefacts
- Dissertation [(pdf)](/files/2022-06-06-capability-protection-scalable-vectors.pdf)
  - [(source code, LuaLaTeX)](https://github.com/theturboturnip/mphil-thesis)
- Summary [(blogpost)](/posts/2022/12/cheri-rvv-rise)
- CHERI-RVV hardware emulator and test programs [(docs)](/files/doc/rsim/index.html)
  - [(source code, Rust + C)](https://github.com/theturboturnip/riscv-v-lite)
- Rust wrapper for the `cheri-compressed-cap` C library [(docs)](/files/doc/rust_cheri_compressed_cap/index.html)
  - [(source code, Rust + C)](https://github.com/theturboturnip/cheri-compressed-cap)
- CHERI-Clang fork, with CHERI-RVV support
  - [(source code, C++)](https://github.com/theturboturnip/llvm-project)


### Presentations
- End-of-year presentation [(pdf)](/files/2022-06-06-capability-protection-scalable-vectors-presentation.pdf)
  - [(source, LuaLaTeX)](https://github.com/theturboturnip/mphil-presentation)
- RISE competition presentation [(youtube, embedded above)](https://www.youtube.com/watch?v=J82OFvF3yGY)
  - [(source, PowerPoint)](/files/2022-09-19-RISE_Presentation.pptx)


## Recommended citation

*Stark, S. (2022). Capability-Based Memory Protection for Scalable Vector Processing. [MPhil thesis]. University of Cambridge. URL: <https://theturboturnip.github.io/files/2022-06-06-capability-protection-scalable-vectors.pdf>*

```
@mastersthesis{starkCapabilityProtectionScalableVectors2022,
    author = "Stark, Samuel",
    title = "Capability-Based Memory Protection for Scalable Vector Processing",
    school = "University of Cambridge",
    year = "2022",
    month = "June",
    url = "https://theturboturnip.github.io/files/2022-06-06-capability-protection-scalable-vectors.pdf"
}
```
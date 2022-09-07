---
title: "Capability-Based Memory Protection for Scalable Vector Processing"
collection: publications
permalink: /academia/2022-06-06-capability-protection-scalable-vectors
redirect_from:
    - /publication/2022-06-06-capability-protection-scalable-vectors
    - /publication/2022-06-06-capability-protection-scalable-vectors.html
    - /mphil
header:
    teaser: "2022-06-06-capability-protection-header-small.png"
excerpt: "On applying CHERI-based memory protection to vector processors, particularly scalable vector models e.g. Arm SVE and RISC-V &quot;V&quot;."
date: 2022-06-06
paperurl: 'https://theturboturnip.github.io/files/2022-06-06-capability-protection-scalable-vectors.pdf'
citation: 'Stark, S. (2021). Capability-Based Memory Protection for Scalable Vector Processing. [M.Phil thesis]. University of Cambridge.'
course: 'Advanced Computer Science M.Phil @ University of Cambridge'
---

<img src='/images/2022-06-06-capability-protection-header-small.png'><br/>

My masters project at University of Cambridge.

Examines the impact of combining CHERI's hardware memory protection with vector processing, particularly vectorized loads and stores, by designing a potential specification for "CHERI-RVV" - a CHERI version of the RISC-V "V" scalable vector extension.

[Download paper here](/files/2022-06-06-capability-protection-scalable-vectors.pdf)

[Download presentation here](/files/2022-06-06-capability-protection-scalable-vectors-presentation.pdf)

Recommended citation BibTeX:
```
@mastersthesis{starkCapabilityProtectionScalableVectors2022,
    author = "Stark, Samuel",
    title = "Capability-Based Memory Protection for Scalable Vector Processing",
    school = "University of Cambridge",
    year = "2022",
    month = "June"
}
```

## Source code
- [RISC-V Vector+CHERI Emulator](https://github.com/theturboturnip/riscv-v-lite)
- [Rust wrapper for `cheri-compressed-cap` C library](https://github.com/theturboturnip/cheri-compressed-cap)
- [CHERI-Clang fork, with CHERI-RVV support](https://github.com/theturboturnip/llvm-project)
- [Thesis](https://github.com/theturboturnip/mphil-thesis)
- Presentation (not available right now)

## Documentation
- [rust-cheri-compressed-cap](/files/doc/rust_cheri_compressed_cap/index.html)
- [riscv-v-lite](/files/doc/rsim/index.html)
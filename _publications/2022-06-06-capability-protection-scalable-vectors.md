---
title: "Capability-Based Memory Protection for Scalable Vector Processing"
collection: publications
permalink: /publication/2022-06-06-capability-protection-scalable-vectors
excerpt: "On applying CHERI-based memory protection to vector processors, particularly scalable vector models e.g. Arm SVE and RISC-V &quot;V&quot;. My masters project at Cambridge."
date: 2022-06-06
paperurl: 'https://theturboturnip.github.io/files/2022-06-06-capability-protection-scalable-vectors.pdf'
citation: 'Stark, Samuel (2021). &quot;Capability-Based Memory Protection
for Scalable Vector Processing&quot; <i>University of Cambridge</i>.'
course: 'Advanced Computer Science M.Phil @ University of Cambridge'
---

<!-- <img src='/images/2021-05-fluid-dynamics-header.png'><br/> -->

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
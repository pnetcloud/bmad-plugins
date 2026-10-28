# Origin

- Original skill: `linkedin-humanizer`
- Public skill: `marketing-linkedin-humanizer`
- Author: Sergey Bulaev
- Source: https://github.com/sergebulaev/linkedin-skills
- Source skill: https://github.com/sergebulaev/linkedin-skills/tree/8f8bc4b40a2d5419b2dcf898772b85712cfbdf41/skills/linkedin-humanizer
- Matching upstream revision: `8f8bc4b40a2d5419b2dcf898772b85712cfbdf41`
- License: MIT; full notice in LICENSE.

Modifications: grouped public identifier and peer references; six-section entry contract with existing topic headings demoted outside code fences; original body rules, workflows and examples retained; shared upstream references and relevant root contract sections included locally with path remapping; host/provider dependencies, private context binding and explicit action authority clarified in DEPENDENCIES.md. Fenced command examples retain upstream CLI names. Original resources retain their relative paths; no provider execution is claimed.

Portability/privacy refinement: the detector example now takes an explicitly resolved installed skill directory while retaining the original script path and arguments. Nonfunctional internal transcript, work-item and notebook provenance pointers were generalized; formula labels, examples, datasets, thresholds and substantive guidance remain available. No detector code, provider bindings or publication policy were changed.

Installed-root cwd correction: the detector setup example now copies `scripts/detectors.env.example` and installs from `requirements-lock.txt` in the same resolved skill root; document-relative file links and authorization guards are unchanged.

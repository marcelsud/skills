# The Depth Tree

Leonxlnx created the Depth Tree as a way to decompose substantial work. Use
depth to separate independently verifiable deliverables. It does not predict
effort or require a particular execution environment.

## Decompose at natural boundaries

Treat the task as the root. Split branches until each leaf has one meaningful
deliverable with clear acceptance criteria. Merge leaves that are only small
mechanical steps. Add depth only when a leaf still contains independently
deliverable outcomes.

Record shared interfaces, ownership, naming, and failure conventions before
dependent work begins. If two leaves change the same artifact or one consumes
the other's result, establish their ordering explicitly.

## Verify each layer

Leaf criteria establish the deliverable's behavior. Branch criteria establish
integration, contract compatibility, and affected related behavior. Verify
children before treating their parent as ready for integration.

Work each leaf through implementation, review, correction, and verification.
Finish when all required criteria have evidence and no blocker or material
issue remains. Cosmetic refinement does not justify another pass.

## Choose an execution approach

A small tree can be completed sequentially by one participant. Larger trees
may use separate participants when available and authorized. The dependency
graph and acceptance criteria stay the same in either approach.

When the user requests a depth, preserve it where it separates real outcomes.
Otherwise choose the shallowest tree that makes deliverables and integration
obligations clear.

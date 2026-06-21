bibkey: atlidakis2019restler
citation: Vaggelis Atlidakis, Patrice Godefroid, Marina Polishchuk. "RESTler: Stateful REST API Fuzzing." Proceedings of the 41st International Conference on Software Engineering (ICSE'19), Montreal, Quebec, Canada, IEEE Press, 2019, pp. 748-758. DOI: 10.1109/ICSE.2019.00083.
doi: 10.1109/ICSE.2019.00083   read: FULL (author copy, patricegodefroid.github.io/public_psfiles/icse2019.pdf, via pdftotext)   access-date: 2026-06-12

CLAIM CARDS

1. Tests are derived FROM the API specification and run against the live service. [verbatim]
   Quote: "RESTler analyzes the API specification of a cloud service and generates sequences of requests that automatically test the service through its API." (Abstract)
   Quote: "performs a lightweight static analysis of an entire Swagger specification, and then generates and executes tests that exercise the corresponding cloud service in a stateful manner." (Sec. I, Introduction)
   Paraphrase: The conformance/test grammar is constructed automatically from the OpenAPI/Swagger document and exercised against the running service -- exactly the "derive tests from the schema, run against the live server" pattern.

2. The spec is compiled into an executable test-generation grammar. [verbatim]
   Quote: "From such a specification, RESTler automatically constructs the test-generation grammar shown on the right of Figure 2. This grammar is encoded in executable python code." (Sec. II)
   Quote (figure caption): "Swagger Specification and Automatically Derived RESTler Grammar." (Fig. 2)
   Paraphrase: The document plane (schema) is mechanically transformed into the runnable exerciser, so the tests cannot drift from the spec -- they are generated from it.

3. The oracle is the unexpected HTTP status code, specifically 500 Internal Server Error. [verbatim]
   Quote: "During fuzzing, RESTler reports each bug, currently defined as a 500 HTTP status code (500 'Internal Server Error') received after executing a request sequence, as soon as it is found." (Sec. V-A)
   Paraphrase: A request sequence that the spec says should succeed but that yields a 500 from the live service is flagged as a bug -- a concrete instance of spec-vs-runtime divergence (the documentation implies a valid call; the runtime is broken).

4. The technique finds real reliability/spec-violation bugs in production services. [verbatim]
   Quote: "We used RESTler to test GitLab ... as well as several Microsoft Azure and Office365 cloud services. RESTler found 28 bugs in GitLab and several bugs in each of the Azure and Office365 cloud services tested so far." (Abstract / Sec. I)
   Paraphrase: Empirically, spec-derived testing against the live runtime surfaces undocumented failures in large, deployed APIs.

5. Scope of the oracle is honestly bounded (relevant to scoping the citation). [verbatim]
   Quote: "RESTler currently can only find bugs defined as unexpected HTTP status codes. Such a simple test oracle cannot detect vulnerabilities that are not visible through HTTP status codes (e.g., 'Information Exposure' and others)." (Sec. V-B, Current Limitations)
   Paraphrase: RESTler's oracle covers status-code drift (incl. 500s / leaked server errors) but does NOT itself check response-body schema conformance (e.g., undocumented keys). That richer response-conformance checking is the natural extension; RESTler establishes the core derive-from-spec-run-against-runtime loop.

METHOD (three sentences)
RESTler statically analyzes an OpenAPI/Swagger specification and compiles it into an executable Python test-generation grammar, inferring producer-consumer dependencies among requests (e.g., resource ids produced by one request and consumed by another). It then generates and executes stateful sequences of HTTP requests against the live service, using dynamic feedback from observed responses to prune invalid combinations and explore reachable states. A request sequence is reported as a bug when the running service returns an unexpected status code (defined as a 500 Internal Server Error), evaluated empirically on GitLab and several Azure/Office365 services.

LIMITATIONS
Authors' own (Sec. V-B): the oracle "can only find bugs defined as unexpected HTTP status codes" and "cannot detect vulnerabilities that are not visible through HTTP status codes"; it does not handle server-side redirects (301/303/307). Consequently RESTler detects status-code-level drift (500s, leaked errors) but not response-body schema mismatches such as undocumented keys -- so it supports the status-code half of the Use Case C oracle directly and the response-shape half only by extension.

CONTRIBUTION (why cited in THIS paper; which claim it supports; verdict)
Cited as the canonical source for automated specification-conformance / REST API testing: an exerciser that derives tests FROM the API spec (document plane) and runs them against the live service (runtime plane) to catch divergence, including 500 Internal Server Errors / leaked server failures. This directly supports Use Case C's "split planes" exerciser pattern. Verdict: SUPPORTED for the spec-derived-testing and status-code/500 drift claim; do not overstate to cover response-body undocumented-key checking, which RESTler explicitly leaves outside its oracle.

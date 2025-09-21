# Changelog

## 0.1.0-alpha.9 (2025-09-20)

Full Changelog: [v0.1.0-alpha.8...v0.1.0-alpha.9](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.8...v0.1.0-alpha.9)

### Features

* improve future compat with pydantic v3 ([a8fac0e](https://github.com/dedalus-labs/dedalus-sdk-python/commit/a8fac0ef8327430609f8bb15db096afecb3883ae))
* **runner:** add conversation history access and instructions parameter ([#15](https://github.com/dedalus-labs/dedalus-sdk-python/issues/15)) ([80d431d](https://github.com/dedalus-labs/dedalus-sdk-python/commit/80d431d07a85d374c9f974e786395596f1ba87a7))
* **types:** replace List[str] with SequenceNotStr in params ([470ee70](https://github.com/dedalus-labs/dedalus-sdk-python/commit/470ee7096075ac6298514ef751a8a6a6e296d0ab))


### Bug Fixes

* avoid newer type syntax ([4c2f6a5](https://github.com/dedalus-labs/dedalus-sdk-python/commit/4c2f6a5fb9de912f51eaceb129404ba2a7de57fc))


### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([b7e06d3](https://github.com/dedalus-labs/dedalus-sdk-python/commit/b7e06d307e626ae5d41189de50697f41c8bebfac))
* **internal:** add Sequence related utils ([9745025](https://github.com/dedalus-labs/dedalus-sdk-python/commit/9745025a9810eebc01de9591d37a099a04184b84))
* **internal:** change ci workflow machines ([733b93d](https://github.com/dedalus-labs/dedalus-sdk-python/commit/733b93d423e6ef1b4a33ae887ca472255afe4963))
* **internal:** codegen related update ([3c37562](https://github.com/dedalus-labs/dedalus-sdk-python/commit/3c37562c59321946e9750170fcef203a9fe15266))
* **internal:** move mypy configurations to `pyproject.toml` file ([ec3d564](https://github.com/dedalus-labs/dedalus-sdk-python/commit/ec3d56422bea912fafe9c43403dde7028fa97f75))
* **internal:** update pydantic dependency ([70ab0cd](https://github.com/dedalus-labs/dedalus-sdk-python/commit/70ab0cdb89b9829a1203cb922dcc7f11474c2cd4))
* **internal:** update pyright exclude list ([72ed0a3](https://github.com/dedalus-labs/dedalus-sdk-python/commit/72ed0a3bf91d86d18dddd90b3e95967cd3443f85))
* **types:** change optional parameter type from NotGiven to Omit ([dc43898](https://github.com/dedalus-labs/dedalus-sdk-python/commit/dc438989d20a3501a99401ffc1f182b8d67672e5))
* update github action ([cb4fefd](https://github.com/dedalus-labs/dedalus-sdk-python/commit/cb4fefd026cd176f56d3b5b12cdaffd2d7ddbdc6))

## 0.1.0-alpha.8 (2025-08-21)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Features

* **api:** id-&gt;name in DedalusModel ([3025957](https://github.com/dedalus-labs/dedalus-sdk-python/commit/3025957f80d8f4dda8c776a8c44598db95ec3065))

## 0.1.0-alpha.7 (2025-08-21)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Features

* **api:** api update ([5375c71](https://github.com/dedalus-labs/dedalus-sdk-python/commit/5375c71f60a9647d4e106faf4b18e07ab48abb49))
* **api:** decouple Model and DedalusModel ([5edd0e7](https://github.com/dedalus-labs/dedalus-sdk-python/commit/5edd0e78e58b523cb729a51a58a9b49a12091ab9))
* **runner:** extract DedalusModel params and warn for unsupported ([#10](https://github.com/dedalus-labs/dedalus-sdk-python/issues/10)) ([905bdd8](https://github.com/dedalus-labs/dedalus-sdk-python/commit/905bdd89db17bcae0ba54f7a38c237f922836cb0))

## 0.1.0-alpha.6 (2025-08-21)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Features

* **api:** api update ([283500e](https://github.com/dedalus-labs/dedalus-sdk-python/commit/283500e638288e248715ac84092727884b0d404d))
* **api:** api update ([769f6d2](https://github.com/dedalus-labs/dedalus-sdk-python/commit/769f6d24cf4458795a2d6a4a1ce5487e24d3b34b))
* **api:** api update ([e8cce59](https://github.com/dedalus-labs/dedalus-sdk-python/commit/e8cce59df56ade2c3be785a4ab68be694b36b325))
* **model:** add DedalusModel ([0bdc7ce](https://github.com/dedalus-labs/dedalus-sdk-python/commit/0bdc7ce32b8c0099d74fbd71afb6c20efc5c2618))

## 0.1.0-alpha.5 (2025-08-18)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Features

* **api:** api update ([8f0cc6e](https://github.com/dedalus-labs/dedalus-sdk-python/commit/8f0cc6eb025ab9c77959390cf26031383bd07001))
* **api:** chat completions ([8ac1a23](https://github.com/dedalus-labs/dedalus-sdk-python/commit/8ac1a23d9c1c37d4de90073dfad6149c83bba2fa))
* **api:** Config update for dedalus-ai/dev ([628cad2](https://github.com/dedalus-labs/dedalus-sdk-python/commit/628cad286ab5da905070f3b8cfb6745b9d9fa29d))
* **api:** dedalus model update ([5556fa3](https://github.com/dedalus-labs/dedalus-sdk-python/commit/5556fa35efbc79ebca565e2cc343b5352c1b10d7))
* **api:** fixing streaming again ([5941d46](https://github.com/dedalus-labs/dedalus-sdk-python/commit/5941d4689192cd099836d201b386ab1503c1fe2b))
* **api:** logic adj ([a45af92](https://github.com/dedalus-labs/dedalus-sdk-python/commit/a45af925e9dcf78e96759532fefdf107f011177e))
* **api:** manual updates ([c4e5b78](https://github.com/dedalus-labs/dedalus-sdk-python/commit/c4e5b787260c849d231961f5cd22369914f41485))
* **api:** ModelConfig ([984626d](https://github.com/dedalus-labs/dedalus-sdk-python/commit/984626d0bc599656a3cdf9c475f4555d1008983a))
* **api:** polished types ([8630870](https://github.com/dedalus-labs/dedalus-sdk-python/commit/863087056b6ccbdcfd40aaf6d4f4e7f203504e97))
* **api:** spec concise ([a38503a](https://github.com/dedalus-labs/dedalus-sdk-python/commit/a38503a65686e3d621f1824536ec1ab6c81515d3))
* **api:** streaming change ([9a6fd36](https://github.com/dedalus-labs/dedalus-sdk-python/commit/9a6fd36da06e70617706dbd4ca4d5a918eea63bb))
* **api:** to_schema and Model class ([3bd4b91](https://github.com/dedalus-labs/dedalus-sdk-python/commit/3bd4b9173773b28ddda3707dfd0dc2fc408dc0a7))
* **api:** update types ([c4baf45](https://github.com/dedalus-labs/dedalus-sdk-python/commit/c4baf451c36f6148aa9e4ab0bc2e8b47c863a8c4))


### Chores

* **internal:** codegen related update ([11afb95](https://github.com/dedalus-labs/dedalus-sdk-python/commit/11afb95b52fbb39f028b3af9671caf5d3971ecb1))
* **internal:** update comment in script ([9c49fad](https://github.com/dedalus-labs/dedalus-sdk-python/commit/9c49fad176ac16c1b204261229a1e385df62df0f))
* update @stainless-api/prism-cli to v5.15.0 ([ce42854](https://github.com/dedalus-labs/dedalus-sdk-python/commit/ce428545f33a6d02b9b1497a2cd93f4af0cb1740))

## 0.1.0-alpha.4 (2025-08-07)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Features

* **api:** streaming schemas ([4a98e16](https://github.com/dedalus-labs/dedalus-sdk-python/commit/4a98e16c5cb406ecabcc30e262299d2eed3517bf))


### Chores

* **internal:** fix ruff target version ([59fdbfc](https://github.com/dedalus-labs/dedalus-sdk-python/commit/59fdbfc95857204f04c35acd156665a54a7825c6))

## 0.1.0-alpha.3 (2025-08-05)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* **api:** add streaming ([745c331](https://github.com/dedalus-labs/dedalus-sdk-python/commit/745c33166a671b79a978961d576064618cc80bcb))
* **api:** add streaming configuration ([0172ad5](https://github.com/dedalus-labs/dedalus-sdk-python/commit/0172ad5175dd15650252a084f213b16c56b8befc))
* **api:** revert streaming for now ([56d57d5](https://github.com/dedalus-labs/dedalus-sdk-python/commit/56d57d5a19034eec13d5a98a86d133d36ac2830a))
* **client:** support file upload requests ([caadecd](https://github.com/dedalus-labs/dedalus-sdk-python/commit/caadecdf5c75297819cd41fe3adcc5f7af3de772))

## 0.1.0-alpha.2 (2025-07-30)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Features

* **api:** api update ([280a595](https://github.com/dedalus-labs/dedalus-sdk-python/commit/280a595b3d3900625cfdf26be12027a88eff9618))

## 0.1.0-alpha.1 (2025-07-30)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/dedalus-labs/dedalus-sdk-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** update via SDK Studio ([9407b44](https://github.com/dedalus-labs/dedalus-sdk-python/commit/9407b44fa8dbd4df7c18c36eab95a5573399810a))

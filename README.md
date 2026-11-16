# labflix/.github

Defaults da organização Labflix: template de pull request, CODEOWNERS da org e **reusable workflows** de governança de PR.

Este repositório permanece **público** para que produtos privados possam chamar os workflows via `uses:` sem PAT.

## Conteúdo

```
.
├── CODEOWNERS
├── pull_request_template.md
├── README.md
├── scripts/
│   └── changelog.py
└── .github/
    └── workflows/          # reusable (on: workflow_call)
        ├── auto-assign.yml
        ├── code-smells.yml
        ├── pr-base-branch.yml
        ├── pr-block-check.yml
        ├── pr-changelog.yml
        ├── pr-review.yml
        └── release-notes.yml
```

Community health files na raiz (`pull_request_template.md`, etc.) continuam como default da org. A lógica de Actions fica só aqui; cada produto mantém um **caller fino**.

Os reusable workflows **precisam** viver em `.github/workflows/` dentro do repositório. Como este repo se chama `.github`, o `uses` fica com o segmento duplicado: `labflix/.github/.github/workflows/<arquivo>@main` — é o formato exigido pelo GitHub, não um erro de path.

## Template de PR

[`pull_request_template.md`](pull_request_template.md) padroniza a descrição da entrega. Fluxo: [documentação do fluxo de trabalho](https://flix-vw2ox3xn.atlassian.net/wiki/x/AQCiBg).

## CODEOWNERS

- **Org:** [`CODEOWNERS`](CODEOWNERS) define `@labflix/Admin_tec`. O mesmo valor aparece em `ORG_DEFAULT_OWNERS` no `pr-review.yml`.
- **Repo:** cada produto pode ter `.github/CODEOWNERS` complementar com `@user` e/ou `@org/team`.
- O pool efetivo é a união org ∪ repo. Basta **1** aprovação elegível (autor e Copilot não contam).

## Workflows reutilizáveis

| Workflow | Função |
|---|---|
| `auto-assign.yml` | Atribui o autor da PR como assignee |
| `code-smells.yml` | Scan SonarQube (baixa artifact `coverage`; o caller faz `needs: test` e passa `SONAR_*`) |
| `pr-base-branch.yml` | Exige base `production` (o caller restringe quando roda) |
| `pr-block-check.yml` | Bloqueia merge se houver `wip` ou label `blocked` |
| `pr-changelog.yml` | Preenche o changelog da PR via `scripts/changelog.py` |
| `pr-review.yml` | Owners org + repo, review e 1 aprovação elegível |
| `release-notes.yml` | Atualiza o draft GitHub Release `Next` |

## Changelog

[`scripts/changelog.py`](scripts/changelog.py) (Python 3 do runner): Conventional Commits → markdown; modos `pr` e `release`. Os workflows fazem checkout deste repo em `.org-github` para executar o script.

## Adoção em um repositório

Não copie a lógica. Crie callers finos, por exemplo:

```yaml
# .github/workflows/pr-review.yml
name: PR review
on:
  pull_request:
    types: [opened, ready_for_review, reopened, synchronize]
  pull_request_review:
    types: [submitted, dismissed]
jobs:
  owner-review:
    uses: labflix/.github/.github/workflows/pr-review.yml@main
    secrets: inherit
```

Repita o padrão para os demais (`auto-assign`, `pr-base-branch`, `pr-block-check`, `pr-changelog`, `release-notes`), com o `on:` adequado em cada caller.

Para Sonar, chame a partir do CI depois do job que publica o artifact `coverage`:

```yaml
# trecho do .github/workflows/ci.yml
sonarqube:
  name: sonarqube
  needs: test
  uses: labflix/.github/.github/workflows/code-smells.yml@main
  secrets: inherit
```

1. Opcional: `.github/CODEOWNERS` complementar.
2. Garanta acesso do time `@labflix/Admin_tec` ao repositório.
3. Na branch protection, marque os checks dos jobs do reusable (`owner-review`, `check-block`, `sonarqube`, etc.).

CI de build/test, Dependabot e afins continuam no produto.

## Referências

- [Fluxo de trabalho](https://flix-vw2ox3xn.atlassian.net/wiki/x/AQCiBg)
- [GitFlow — Downstream](https://flix-vw2ox3xn.atlassian.net/wiki/spaces/DDS/pages/111280129/GitFlow+-+Fluxo+de+trabalho+no+Downstream)
- [Qualidade de código](https://flix-vw2ox3xn.atlassian.net/wiki/x/AYCFFg)
- [Reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

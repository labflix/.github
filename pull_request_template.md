# Pull Request

A qualidade do código é responsabilidade compartilhada. Ao aprovar, o revisor declara que leu o diff, concorda com a solução e assume o impacto do que passou. Fluxo: [documentação do fluxo de trabalho](https://flix-vw2ox3xn.atlassian.net/wiki/x/AQCiBg).


## Entrega

https://flix-vw2ox3xn.atlassian.net/browse/DEVLBX-000

<!-- O que muda e por quê, em uma ou duas frases -->


### Variáveis de ambiente, feature toggles, remote configs

- N/A

<!-- LABFLIX_ENV_NAME -->


### Recursos de infraestrutura (tickets bloqueantes para queries, env vars, etc)

N/A

<!-- https://flix-vw2ox3xn.atlassian.net/servicedesk/customer/portal/67/INFRA-000 |  -->

### Bloqueios por outras entregas (N/A, um ou muitos)

N/A

<!-- Depends on: <https://github.com/labflix/<repo>/pull/00> -->


### Como testar

1. ...

<!-- Caminho feliz, erro e borda. Sem cache, env local ou dado mágico. -->


## Changelog

<!-- Gerado pelos commits da branch. Não edite o bloco. -->
<!-- changelog:start -->
N/A
<!-- changelog:end -->


## Checklist do revisor

<!-- Somente o revisor marca. Deixe desmarcado. -->

- [ ] O título segue `TICKET - Descrição clara da mudança`
- [ ] [A branch segue o gitflow (`feature/`, `fix/`, `release/`, `release-fix/`, `release-merge/<ticket>-<ambiente>`, `hotfix/<data>`) e nasceu da origem correta para o tipo dela](https://flix-vw2ox3xn.atlassian.net/wiki/spaces/DDS/pages/111280129/GitFlow+-+Fluxo+de+trabalho+no+Downstream#Branches-de-trabalho-e-entrega)
- [ ] O link do Jira corresponde ao código e a PR tem uma responsabilidade só
- [ ] Li o diff (exceto gerados) e a solução é a mais simples para o ticket, sem mudança oportunista
- [ ] [Nomes são claros, o código não duplica nem acopla, e contratos existentes continuam válidos](https://flix-vw2ox3xn.atlassian.net/wiki/x/AYCFFg)
- [ ] Supressão de linter (`biome-ignore` e equivalentes) tem justificativa no diff
- [ ] O teste descrito cobre o caminho, o erro e a borda, sem depender de cache ou dado local
- [ ] Envs, tickets de suporte e recursos listados estão completos e já existem no ambiente alvo, quando a PR precisa deles
- [ ] [Conflito, se houve, foi resolvido fora da interface do GitHub](https://flix-vw2ox3xn.atlassian.net/wiki/spaces/DDS/pages/111280129/GitFlow+-+Fluxo+de+trabalho+no+Downstream#O-que-fazer-em-caso-de-CONFLITO%3F)
- [ ] Li o código, a qualidade não baixou e a responsabilidade é compartilhada entre autor e revisores

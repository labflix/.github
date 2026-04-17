# 📌 Pull Request Checklist

> ⚠️ **IMPORTANTE**  
> A qualidade e a correção do código são uma **RESPONSABILIDADE COMPARTILHADA**.  
>  
> **Autor da PR:** Ajude na revisão! Atente-se às branches usadas, conflitos, descrição completa da PR e fluxo de trabalho.  
>  
> **Revisor da PR:** Revise com atenção! Atente-se à descrição bem preenchida desta PR, veja se as branches estão corretas e seguem o fluxo de trabalho documentado, veja se na lista de commits não há merges incorretos, leia o código atentamente e compare com o que foi solicitado pelo link do Jira!  
>  
> **Autor e Revisor:** não deixem de usar o Copilot para ajudar no review, principalmente quando a PR for muito grande.  
>  
>  Em caso de dúvidas, consulte a **[documentação do fluxo de trabalho](https://flix-vw2ox3xn.atlassian.net/wiki/x/AQCiBg)**, consulte seus colegas e o seu superior imediato.

---

## 📎 Informações sobre a entrega

<!-- Informe o link da história ou sub-tarefa no Jira -->
https://SEU-JIRA/browse/ABC-123

### Variáveis de ambiente (envs), feature toggles, remote configs etc. introduzidas, alteradas ou removidas:

<!-- Liste aqui a variável, seu valor (se não for secreto) e se já foi aplicado no ambiente, ou deixe o "N/A" -->
- N/A

### Criação ou alteração de Recursos de Infraestrutura necessários (buckets, tabelas, etc.):

<!-- Liste aqui o recurso e se já foi aplicado no ambiente alvo, ou deixe o "N/A" -->
- N/A

### PRs anteriores desta mesma entrega:

<!-- Liste aqui as PRs para release, dev e/ou homol, ou deixe o "N/A" se esta for a primeira PR -->
- N/A

## ✅ Checklists  

### 🧭 AUTOR DA PR: preencha este checklist antes do code review!

> Revisor, se **qualquer** item abaixo não estiver correto, **NÃO INICIE O CODE REVIEW**.  
> Solicite ajustes ao autor da PR.

- [ ] O nome da branch origem (from, compare) segue **exatamente** o padrão definido:
  - feature/ABC-123
  - bugfix/ABC-123
  - hotfix/ABC-123
  - release/ABC-123
- [ ] A branch origem **NÃO** foi criada a partir de dev ou homol
- [ ] Não existem commits de merge de dev ou homol
- [ ] O título da PR segue o padrão: "ABC-123 - Título da história no Jira"
- [ ] A PR possui **apenas uma responsabilidade clara** (exatamente o solicitado no link do Jira)
- [ ] A PR não está marcada como WIP / Draft
- [ ] Variáveis de ambiente, recursos de infra, alterações de banco etc. foram devidamente listados acima

### 🔍 REVISOR DA PR: preencha durante o Code Review (leitura obrigatória)

> ⚠️ **Não aprove PRs por hábito, pressa ou confiança pessoal.**

- [ ] **Li todos os arquivos modificados**, exceto arquivos gerados automaticamente
- [ ] **Entendi o porquê de cada mudança**, não apenas “o que foi feito”
- [ ] O código resolve **exatamente** o que está descrito no Jira — nem mais, nem menos
- [ ] Não há código comentado, temporário ou “pra depois”
- [ ] Não foram adicionados `console.log`, `debugger`, logs temporários ou código morto
- [ ] Não foram adicionados `eslint-disable`, `@ts-ignore` ou similares sem justificativa clara
- [ ] Nomes de variáveis, funções, arquivos e componentes são claros e consistentes
- [ ] O código é legível por alguém que **não participou do desenvolvimento**
- [ ] Não existe duplicação de lógica ou código sem justificativa clara
- [ ] O código segue os padrões e convenções do projeto
- [ ] Esta PR **não contamina o histórico** de branches release/, hotfix/ ou production
- [ ] A solução implementada é a mais simples / eficiente para o que se busca
- [ ] Sugestões do Copilot foram cuidadosamente analisadas / implementadas

## 🧾 Declaração final do revisor (obrigatória)

> ⚠️ Ao marcar os itens abaixo, o revisor assume responsabilidade técnica.

- [ ] Declaro que **li e revisei conscientemente todo o código desta PR**

## ℹ️ Observações importantes sobre este checklist

- Este checklist não pode ser adulterado! Consulte a [checklist original](https://github.com/labflix/.github/blob/main/pull_request_template.md).
- Aprovar uma PR sem leitura do código é **falha grave de processo!**
- Se algo parecer errado, estranho ou difícil de entender, **questione!**

> **Revisor, esta é sua chance de contribuir com esta entrega! Capriche ;D**

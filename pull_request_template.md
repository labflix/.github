# 📌 Pull Request Checklist

> ⚠️ **IMPORTANTE**  
> A qualidade e a correção do código são uma **RESPONSABILIDADE COMPARTILHADA**.
>  
> Ao aprovar este PR, o revisor declara explicitamente que:
>  
> - Todas as linhas de código relevantes foram lidas e compreendidas.  
> - O revisor concorda com a solução, não apenas com o resultado.  
> - Qualquer bug, regressão ou problema de design que não tenha sido identificado aqui também é de responsabilidade do revisor.  

---

## 📎 Informações Jira

<!-- Informe o link da história ou sub-tarefa no Jira -->
https://SEU-JIRA/browse/ABC-123

---

## ✅ Checklists  
<!-- ⚠️ O checklist deve ser preenchido APENAS pelo REVISOR -->

---

## 🧭 Antes do Code Review (bloqueante)

> Se **qualquer** item abaixo não estiver correto, **NÃO INICIE O CODE REVIEW**.  
> Solicite ajustes ao autor da PR.

- [ ] O nome da branch segue **exatamente** o padrão definido:
  - feature/ABC-123
  - bugfix/ABC-123
  - hotfix/ABC-123
  - release/ABC-123
- [ ] A branch **NÃO** foi criada a partir de dev ou homol (somente production)
- [ ] O título da PR segue o padrão: ABC-123 - Descrição clara e objetiva da mudança
- [ ] O link da task no Jira foi informado e corresponde ao código alterado
- [ ] A PR possui **apenas uma responsabilidade clara**
- [ ] Não existem commits de merge de:
  - dev
  - homol
- [ ] A PR não está marcada como WIP / Draft
- [ ] O autor da PR está corretamente definido como responsável (Assignee)

---

## 🔍 Durante o Code Review (leitura obrigatória)

> ⚠️ **Não aprove PRs por hábito, pressa ou confiança pessoal.**

- [ ] **Li todos os arquivos modificados**, exceto arquivos gerados automaticamente
- [ ] **Entendi o porquê de cada mudança**, não apenas “o que foi feito”
- [ ] O código resolve **exatamente** o que está descrito no Jira — nem mais, nem menos
- [ ] Não existem mudanças “aproveitando a PR” (refactors oportunistas)
- [ ] Não há código comentado, temporário ou “pra depois”
- [ ] Não foram adicionados `console.log`, `debugger`, logs temporários ou código morto
- [ ] Não foram adicionados `eslint-disable`, `@ts-ignore` ou similares sem justificativa **documentada**
- [ ] Nomes de variáveis, funções, arquivos e componentes são claros e consistentes
- [ ] O código é legível por alguém que **não participou do desenvolvimento**
- [ ] Não existe duplicação de lógica que poderia ser reutilizada
- [ ] O código segue os padrões e convenções do projeto

---

## 🧠 Qualidade, arquitetura e impacto

- [ ] A solução escolhida é a **mais simples possível** para o problema
- [ ] Não há impacto negativo de performance evidente
- [ ] Não há impacto negativo de segurança evidente
- [ ] Não foram introduzidas dependências desnecessárias
- [ ] Não foram quebrados contratos existentes (APIs, props, hooks, etc.)
- [ ] O código não introduz acoplamento desnecessário
- [ ] O código não dificulta testes ou manutenção futura

---

## 🧪 Testes e validação

- [ ] O código foi testado manualmente pelo autor
- [ ] O revisor entende **como** testar essa mudança
- [ ] Casos de erro e bordas (edge cases) foram considerados
- [ ] Não há dependência implícita de estado externo (cache, env local, dados mágicos)
- [ ] O comportamento em dev/homol é previsível e consistente

---

## 🌱 Variáveis de ambiente / Configurações

- [ ] Variáveis de ambiente novas, alteradas ou removidas foram listadas abaixo
- [ ] As variáveis estão documentadas (nome, propósito e impacto)
- [ ] Não existem segredos hardcoded no código
- [ ] Flags, configs remotas ou feature toggles estão corretamente descritas

### Variáveis de ambiente (envs)

<!-- Liste aqui ou escreva "N/A" -->
- N/A

---

## 🚫 Regras de workflow (CRÍTICAS)

- [ ] Nenhum conflito foi resolvido diretamente na PR via GitHub
- [ ] Nenhum commit direto foi feito em:
  - dev
  - homol
  - production
  - release/*
- [ ] Nenhum squash ou rebase foi realizado fora de production
- [ ] Esta PR **não** contamina histórico de outras branches

---

## 🧾 Declaração final do revisor (obrigatória)

> ⚠️ Ao marcar os itens abaixo, o revisor assume responsabilidade técnica.

- [ ] Declaro que **li e revisei conscientemente todo o código desta PR**
- [ ] Declaro que o nível de qualidade do projeto **não foi reduzido**
- [ ] Declaro que, se este código causar problemas futuros, reconheço que
    **a responsabilidade é compartilhada entre autor e revisores**

---

## ℹ️ Observações importantes sobre este checklist

- Este checklist deve ser preenchido **somente pelo REVISOR**
- Aprovar uma PR sem leitura completa é **falha grave de processo**
- Confiança pessoal **não substitui** revisão técnica
- “Depois a gente arruma” **não é aceitável**
- Se algo parecer errado, **questione**, mesmo que o autor seja sênior

---

> **Code review não é aprovação social.  
> É um contrato de responsabilidade compartilhada.**

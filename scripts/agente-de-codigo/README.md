# agente-de-codigo — documentação automática

Agente que mantém a **documentação do projeto no vault do Obsidian** sincronizada com o código, **sozinho, a cada commit**. Ele documenta o que mudou e atualiza envs/senhas quando necessário — você nunca precisa pedir.

> Companheiro do `clube-do-gole-marketing`: um cuida de conteúdo, este cuida de código/documentação.

---

## Como funciona

```
 git commit
     │
     ▼
 .git/hooks/post-commit   (dispara em background, NUNCA bloqueia o commit)
     │   salva o diff em .git/agente-de-codigo-last-diff.txt
     │   exporta CLAUDE_CODE_OAUTH_TOKEN (de .git/agente-de-codigo.token)
     ▼
 claude.exe -p "..."  --permission-mode bypassPermissions  --add-dir <vault>
     │   (usa o agente ~/.claude/agents/agente-de-codigo.md, model: sonnet)
     ▼
 Vault do Obsidian
   ├─ Docs/*.md     ← atualiza a documentação técnica afetada
   ├─ Envs.md       ← sincroniza se mudaram variáveis de ambiente
   └─ Senhas.md     ← sincroniza se mudaram credenciais/integrações
     │
     ▼
 .git/agente-de-codigo.log   (resumo do que foi feito)
```

**Regras do agente:** só escreve dentro do vault; **nunca** edita código, **nunca** commita, **nunca** apaga arquivos ou remove segredos reais.

### Peças

| Peça | Onde | Versionado? |
|------|------|-------------|
| Definição do agente | `~/.claude/agents/agente-de-codigo.md` | Não (por máquina) |
| Git hook | `<repo>/.git/hooks/post-commit` | Não (`.git/` não é clonado) |
| Token OAuth | `<repo>/.git/agente-de-codigo.token` | **Não — é segredo** |
| Templates + instalador | `scripts/agente-de-codigo/` | **Sim** (vai no clone) |

Como o agente, o hook e o token vivem **fora** dos arquivos versionados, cada máquina precisa rodar o instalador uma vez.

---

## Instalar em outra máquina

Pré-requisitos: **Git**, o app **Claude Code** instalado e uma conta Claude (Pro/Max), e o **vault** acessível (ex.: Google Drive sincronizado).

```powershell
# 1) clone o repo e entre nele
git clone <url-do-repo> ; cd Clube_do_gole

# 2) rode o instalador (ajuste -VaultPath se o vault não estiver em G:)
.\scripts\agente-de-codigo\install.ps1
# ou:
.\scripts\agente-de-codigo\install.ps1 -VaultPath "D:\Drive\Clube do Gole - Full\05 - Produto & Tecnologia"
```

O instalador vai:
1. Copiar o agente para `~/.claude/agents/`.
2. Instalar o hook `post-commit` no repo.
3. Pedir o **token OAuth** — quando solicitado, abra outra janela e rode
   `& "<caminho-do-claude>" setup-token`, autorize no navegador e cole o token (`sk-ant-oat01-...`).
4. Testar a autenticação headless.

Depois disso, todo commit dispara o agente automaticamente.

---

## Uso e manutenção

- **Ver o que ele fez:** `.git/agente-de-codigo.log`
- **Pular num commit específico:** `git commit --no-verify`
- **Desligar de vez:** apague `.git/hooks/post-commit`
- **Rodar manualmente** (regenerar/forçar revisão): chame o agente `agente-de-codigo` pelo Claude Code e peça a revisão desejada.
- **Token expira em 1 ano:** rode `setup-token` de novo e atualize `.git/agente-de-codigo.token`.

## Notas (Windows)

- O app Claude é empacotado (Store/MSIX). O `claude.exe` real fica em
  `%LOCALAPPDATA%\Packages\*laude*\LocalCache\Roaming\Claude\claude-code\<versão>\claude.exe`.
  O hook e o instalador resolvem esse caminho automaticamente.
- O login do app **não** é compartilhado com o CLI headless — por isso usamos o token OAuth via `CLAUDE_CODE_OAUTH_TOKEN`.

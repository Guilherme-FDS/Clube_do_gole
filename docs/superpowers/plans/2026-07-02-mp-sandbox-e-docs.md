# Mercado Pago Sandbox + Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer o checkout exigir e validar pagamento de teste real do Mercado Pago (cartão/pix/boleto fictícios) antes de aprovar a venda, com documentação clara pra banca testar, e o botão de aprovação manual do admin virando explicitamente uma exceção.

**Architecture:** Nenhuma mudança na lógica de `mercadopago_service.py`/webhook — já está correta (detecta credencial de teste vs produção, só aprova via webhook real). O trabalho é: (1) trocar a credencial no Render pra uma de teste (ação manual do usuário, guiada), (2) deixar o botão de aprovação manual do admin claramente marcado como bypass, (3) documentar cartões/pix/boleto de teste nos READMEs dos dois repos.

**Tech Stack:** Vue 3 (admin, site), Markdown (docs).

**Repos:**
- Site: `C:\Users\Guilherme Silva\Desktop\Projetos\Clube_do_gole\site\Clube_do_gole` (branch `main`) — Tasks 2, 3
- Mobile: `C:\Users\Guilherme Silva\Desktop\Projetos\Clube_do_gole\mobile` (branch `master`) — Task 4
- Ação manual do usuário (fora de código) — Task 1

---

### Task 1: [AÇÃO MANUAL] Gerar credenciais de teste do Mercado Pago e trocar no Render

**Não é uma task de código — é um checklist guiado, feito junto com o usuário.**

- [ ] **Step 1: Gerar credenciais de teste**

No painel [Mercado Pago Developers](https://www.mercadopago.com.br/developers/panel/app) → sua aplicação → aba **"Credenciais de teste"** (não "Credenciais de produção"). Copiar:
- `Access Token` (começa com `TEST-`)
- `Public Key` (começa com `TEST-`)

- [ ] **Step 2: Criar usuário de teste comprador (se ainda não tiver)**

No mesmo painel → **"Contas de teste"** → criar uma conta de teste tipo "comprador" (`TESTUSER...`), separada da conta vendedora. É essa conta de teste que "compra" com os cartões fictícios — não precisa logar nela de verdade, o cartão fictício funciona sem precisar de login especial no MP.

- [ ] **Step 3: Trocar as env vars no Render**

Painel Render → serviço `clube-do-gole-backend` → **Environment** → editar:
- `MP_ACCESS_TOKEN` → cola o valor `TEST-...` do Step 1
- `MP_PUBLIC_KEY` → cola o valor `TEST-...` do Step 1 (não é usado pelo código hoje, mas mantém documentado/atualizado)

Salvar → Render redeploya sozinho.

- [ ] **Step 4: Confirmar**

Depois do redeploy, um checkout de teste deve abrir a URL de **sandbox** do Mercado Pago (a página de teste tem uma faixa/aviso "Modo de teste" visível). Se abrir a página de produção normal (sem aviso de teste), a credencial não foi trocada corretamente — conferir de novo no Render.

---

### Task 2: Botão "Aprovar venda" manual vira claramente uma exceção

**Files:**
- Modify: `frontend/src/views/admin/Detalhesvenda.vue`

- [ ] **Step 1: Trocar label, estilo e confirmação do botão**

Encontrar o bloco do botão (dentro do `page-header`):

```html
          <button
            v-if="venda.status === 'pendente'"
            @click="aprovarVenda"
            :disabled="aprovando"
            class="btn-aprovar"
          >
            <i :class="aprovando ? 'fas fa-spinner fa-spin' : 'fas fa-check'"></i>
            {{ aprovando ? 'Aprovando...' : 'Aprovar venda' }}
          </button>
```

Substituir por:

```html
          <button
            v-if="venda.status === 'pendente'"
            @click="aprovarVenda"
            :disabled="aprovando"
            class="btn-aprovar"
            title="Pula a validação real do Mercado Pago — use só em caso excepcional (ex: boleto pago fisicamente e o webhook atrasou)"
          >
            <i :class="aprovando ? 'fas fa-spinner fa-spin' : 'fas fa-exclamation-triangle'"></i>
            {{ aprovando ? 'Aprovando...' : '⚠️ Aprovar manualmente (bypass)' }}
          </button>
```

- [ ] **Step 2: Atualizar o texto de confirmação em `aprovarVenda()`**

Encontrar:
```js
const aprovarVenda = async () => {
  if (!confirm('Aprovar esta venda manualmente? Isso criará a assinatura do cliente.')) return
```

Substituir por:
```js
const aprovarVenda = async () => {
  if (!confirm('⚠️ Isso PULA a validação real do Mercado Pago e ativa a assinatura na hora, sem confirmar se o pagamento realmente aconteceu.\n\nUse só em casos excepcionais (ex: boleto físico já pago, webhook atrasado).\n\nConfirma mesmo assim?')) return
```

- [ ] **Step 3: Trocar a cor do botão pra amarelo/aviso (não mais verde)**

Encontrar no `<style scoped>`:
```css
.btn-aprovar {
  background: #2E8B57;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}
.btn-aprovar:hover:not(:disabled) { background: #246b44; }
.btn-aprovar:disabled { opacity: 0.6; cursor: not-allowed; }
```

Substituir por:
```css
.btn-aprovar {
  background: #FEF3C7;
  color: #92400E;
  border: 1px solid #F59E0B;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}
.btn-aprovar:hover:not(:disabled) { background: #FDE68A; }
.btn-aprovar:disabled { opacity: 0.6; cursor: not-allowed; }
```

- [ ] **Step 4: Verificar manualmente**

Sem suite de testes do frontend Vue. Ler o arquivo final e confirmar: botão amarelo/aviso, ícone de exclamação, texto "⚠️ Aprovar manualmente (bypass)", confirmação explicando que pula a validação real.

- [ ] **Step 5: Commit e push**

```bash
git add frontend/src/views/admin/Detalhesvenda.vue
git commit -m "feat: deixa aprovacao manual de venda claramente marcada como bypass"
git push origin main
```
Adicionar `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` como última linha do corpo do commit.

---

### Task 3: [SITE] README — seção "Testando pagamentos"

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Adicionar nova seção ao final do README**

Ler o README atual pra achar um bom lugar (antes da seção de licença/contribuição, se houver, ou no final do arquivo). Adicionar:

```markdown
---

## Testando pagamentos (Mercado Pago sandbox)

O checkout usa o **Checkout Pro** do Mercado Pago. Em produção com credencial de teste (`MP_ACCESS_TOKEN` começando com `TEST-`), o link de pagamento abre a página de **sandbox** do MP — nenhum dinheiro real é movimentado, mas o fluxo completo (validação de cartão, PIX, boleto e webhook) roda de verdade.

### Cartões de crédito de teste (Brasil)

| Bandeira | Número | CVV | Validade | Nome do titular | Resultado |
|---|---|---|---|---|---|
| Mastercard | 5031 4332 1540 6351 | 123 | 11/30 | APRO | Aprovado |
| Visa | 4235 6477 2802 5682 | 123 | 11/30 | APRO | Aprovado |
| Visa | 4013 5406 8274 6260 | 123 | 11/30 | OTHE | Recusado (fundos insuficientes) |

O nome do titular controla o resultado no sandbox: `APRO` sempre aprova, `OTHE` sempre recusa — é a convenção oficial do Mercado Pago pra teste, não precisa de cartão real nenhum.

CPF de teste: qualquer CPF numericamente válido (ex: gerado em [4devs.com.br/gerador_de_cpf](https://www.4devs.com.br/gerador_de_cpf)).

### PIX de teste

No sandbox, o QR Code gerado é fictício. Pra simular a confirmação do pagamento, entra na conta de teste "vendedora" no painel do Mercado Pago (Sandbox → Pagamentos) e usa o botão de simular aprovação — não precisa de app de banco real.

### Boleto de teste

Mesma lógica do PIX: o boleto gerado no sandbox é fictício, e o próprio painel de testes do Mercado Pago permite simular o pagamento manualmente.

### Onde configurar

Env vars `MP_ACCESS_TOKEN` / `MP_PUBLIC_KEY` (backend) — usar as credenciais de **teste** (prefixo `TEST-`), geradas em [Mercado Pago Developers → Suas integrações → Credenciais de teste](https://www.mercadopago.com.br/developers/panel/app). Nunca comitar essas chaves — ficam só em variáveis de ambiente (Render).

> Documentação oficial de cartões de teste (pode mudar): https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/additional-content/your-integrations/test/cards
```

- [ ] **Step 2: Commit e push**

```bash
git add README.md
git commit -m "docs: adiciona secao de cartoes/pix/boleto de teste do Mercado Pago"
git push origin main
```
Adicionar `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` como última linha.

---

### Task 4: [MOBILE] README — seção "Testando pagamentos"

**Files:**
- Modify: `README.md` (repo mobile)

- [ ] **Step 1: Ler o README atual do mobile e adicionar a mesma seção**

Adicionar ao final do arquivo (mesmo conteúdo do Task 3, adaptado pro contexto do app):

```markdown
---

## Testando pagamentos (Mercado Pago sandbox)

O fluxo de checkout do app (Carrinho → Checkout → "Ir para pagamento") abre o link do Mercado Pago no navegador do celular. Com o backend configurado com credencial de **teste** (`MP_ACCESS_TOKEN` começando com `TEST-`), essa página é o sandbox do MP — nenhum dinheiro real é movimentado.

### Cartões de crédito de teste (Brasil)

| Bandeira | Número | CVV | Validade | Nome do titular | Resultado |
|---|---|---|---|---|---|
| Mastercard | 5031 4332 1540 6351 | 123 | 11/30 | APRO | Aprovado |
| Visa | 4235 6477 2802 5682 | 123 | 11/30 | APRO | Aprovado |
| Visa | 4013 5406 8274 6260 | 123 | 11/30 | OTHE | Recusado |

Nome do titular `APRO` aprova, `OTHE` recusa — convenção do sandbox do Mercado Pago.

### PIX e boleto de teste

Ambos gerados como fictícios no sandbox. Simule a aprovação manualmente pelo painel de testes do Mercado Pago (conta vendedora → Sandbox → Pagamentos).

Depois de "pagar" no sandbox, volte pro app e confira em Perfil → Meus pedidos — o status muda pra "Pago" automaticamente assim que o webhook do backend processar a confirmação (pode levar alguns segundos).

> Documentação oficial (pode mudar): https://www.mercadopago.com.br/developers/pt/docs/checkout-pro/additional-content/your-integrations/test/cards
```

- [ ] **Step 2: Commit e push**

```bash
git add README.md
git commit -m "docs: adiciona secao de teste de pagamentos Mercado Pago (sandbox)"
git push origin master
```
Adicionar `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` como última linha.

---

### Task 5: Verificação final

- [ ] **Step 1: Confirmar Task 1 (credenciais) foi feita**

Sem isso, nada do resto funciona de verdade — é pré-requisito real pro teste da banca.

- [ ] **Step 2: Fazer uma compra de teste de ponta a ponta**

App/site → Assinar → Carrinho → Checkout → "Ir para pagamento" → cartão de teste `APRO` → volta pro app/site → conferir que o pedido aparece como "Pago" (não precisou clicar em nada no admin) e que o método aparece corretamente (Cartão de Crédito) na tela de Pagamentos do admin.

- [ ] **Step 3: Confirmar botão de aprovação manual está com o novo visual**

Abrir uma venda pendente no admin → confirmar botão amarelo "⚠️ Aprovar manualmente (bypass)".

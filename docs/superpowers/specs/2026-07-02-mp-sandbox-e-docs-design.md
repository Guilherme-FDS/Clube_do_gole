# Mercado Pago sandbox + validação correta de pagamento — Design

Data: 2026-07-02
Status: aprovado pelo usuário

## Contexto

Projeto vai passar por banca de avaliação. Precisa demonstrar checkout funcionando de ponta a ponta com Mercado Pago, exigindo dados de cartão/pix/boleto fictícios antes de aprovar a venda — não pode aprovar automaticamente sem passar pelo teste real do MP.

## Diagnóstico (já confirmado por pesquisa no código)

- `backend/services/mercadopago_service.py::criar_preferencia()` **já detecta** se o `MP_ACCESS_TOKEN` começa com `TEST-` (retorna `sandbox_init_point`) ou `APP_USR-` (retorna `init_point` de produção). Nenhuma mudança de código necessária aqui.
- Credencial hoje no Render é de **produção** (`APP_USR-...`) — por isso os cartões fictícios de teste do Mercado Pago não funcionam.
- Webhook (`POST /api/pagamentos/webhook`) já busca o pagamento real na API do MP, atualiza `metodo`/`status` no banco, e só chama `aprovar_venda()` (que ativa a assinatura) quando o status vier "aprovado". Fluxo já é correto.
- Campo `metodo` fica "outro" hoje porque nenhuma venda passou pelo webhook real ainda (sempre foi via botão manual do admin ou modo dev sem MP configurado) — não é bug de mapeamento, é falta de um pagamento real de teste ainda ter acontecido.
- `POST /admin/vendas/{id}/aprovar` (botão "Aprovar venda" manual) pula toda essa validação e ativa a assinatura na hora.

## Decisões

### 1. Trocar credenciais no Render pra TEST- (ação do usuário, não código)
Vou guiar a gerar as credenciais de teste no painel Mercado Pago Developers (aba "Suas integrações" → aplicação → credenciais de teste). Depois troco eu mesmo as env vars no Render.

### 2. Botão "Aprovar venda" manual vira claramente uma exceção
Mantém funcional (útil pra boleto físico que demora, ou emergência), mas:
- Label muda pra `⚠️ Aprovar manualmente (pula validação do Mercado Pago)`
- Confirmação (`window.confirm` ou modal) antes de executar, deixando explícito que é bypass
- Estilo visual diferenciado (vermelho/aviso, não mais botão primário verde/dourado)

### 3. Nenhuma mudança no mapeamento de método de pagamento
Já funciona — só precisa de uma venda real passando pelo sandbox pra popular certo.

### 4. README novo: seção "Testando pagamentos" em **ambos os repos** (site e mobile)
Conteúdo (cartões oficiais de teste do Mercado Pago Brasil, documentados publicamente pela própria MP):

**Cartões de crédito de teste:**
| Bandeira | Número | CVV | Validade | Resultado |
|---|---|---|---|---|
| Mastercard | 5031 4332 1540 6351 | 123 | 11/30 | Aprovado |
| Visa | 4235 6477 2802 5682 | 123 | 11/30 | Aprovado |
| Visa (recusado) | 4013 5406 8274 6260 | 123 | 11/30 | Recusado (fundos insuficientes) |

Nome do titular: `APRO` (aprova automaticamente) ou `OTHE` (recusa) — convenção oficial do MP sandbox.
CPF de teste: qualquer CPF válido gerado (ex: gerador online), ou `123.456.789-09` (comumente aceito em sandbox).

**PIX de teste**: no sandbox, o QR code gerado é fictício — o próprio painel do Mercado Pago (conta de teste "vendedor") tem um botão pra simular a confirmação do PIX manualmente.

**Boleto de teste**: sandbox gera um boleto fictício; o painel de testes do MP permite simular o pagamento (mesma lógica do PIX).

Link oficial da documentação do MP sobre cartões de teste, pra manter atualizado se a MP mudar os números.

## Fora de escopo
- Mudar o SDK de `httpx` pra SDK oficial do MP (funciona bem como está)
- Restringir métodos de pagamento na preferência (deixa MP mostrar o que a conta permite, já é o comportamento hoje)
- Usar `MP_PUBLIC_KEY` no frontend (não é usado hoje e não é necessário pro Checkout Pro via redirect)

## Critérios de aceite
1. Com credencial TEST- configurada, `checkout_url` retornado é a URL de sandbox do MP
2. Completar um pagamento de teste (cartão aprovado) faz o webhook disparar, `metodo` populado corretamente, assinatura ativada automaticamente — sem clicar em nada no admin
3. Botão de aprovação manual continua funcional mas com aviso visual claro de que é bypass
4. README do site e do mobile têm a seção "Testando pagamentos" com os cartões/PIX/boleto de teste

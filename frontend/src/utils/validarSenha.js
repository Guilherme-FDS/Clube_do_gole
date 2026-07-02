export function validarSenha(s) {
  if (!s || s.length < 8) return 'A senha deve ter no mínimo 8 caracteres.'
  if (!/[A-Z]/.test(s)) return 'A senha deve conter ao menos uma letra maiúscula.'
  if (!/[a-z]/.test(s)) return 'A senha deve conter ao menos uma letra minúscula.'
  if (!/[0-9]/.test(s)) return 'A senha deve conter ao menos um número.'
  return null
}

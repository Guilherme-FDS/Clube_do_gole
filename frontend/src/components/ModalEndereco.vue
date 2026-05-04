<template>
  <div v-if="aberto" class="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ editando ? 'Editar Endereço' : 'Adicionar Novo Endereço' }}</h3>
        <button class="modal-close" @click="$emit('fechar')"><i class="fas fa-times"></i></button>
      </div>

      <form class="endereco-form" @submit.prevent="salvar">
        <div class="form-group">
          <label>CEP *</label>
          <input v-model="form.cep" type="text" maxlength="9" required @blur="buscarCEP" />
        </div>
        <div class="form-grid">
          <div class="form-group">
            <label>Endereço *</label>
            <input v-model="form.endereco" type="text" required />
          </div>
          <div class="form-group">
            <label>Número *</label>
            <input v-model="form.numero" type="text" required />
          </div>
        </div>
        <div class="form-group">
          <label>Complemento</label>
          <input v-model="form.complemento" type="text" placeholder="Apartamento, bloco, etc." />
        </div>
        <div class="form-grid">
          <div class="form-group">
            <label>Bairro *</label>
            <input v-model="form.bairro" type="text" required />
          </div>
          <div class="form-group">
            <label>Cidade *</label>
            <input v-model="form.cidade" type="text" required />
          </div>
        </div>
        <div class="form-grid">
          <div class="form-group">
            <label>Estado *</label>
            <select v-model="form.estado" required>
              <option value="">Selecione</option>
              <option v-for="uf in ufs" :key="uf.v" :value="uf.v">{{ uf.l }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>País *</label>
            <input v-model="form.pais" type="text" required />
          </div>
        </div>
        <div class="form-group checkbox-group">
          <input v-model="form.principal" type="checkbox" id="endereco_principal" />
          <label for="endereco_principal">Tornar este endereço principal</label>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="$emit('fechar')">Cancelar</button>
          <button type="submit" class="btn-primary" :disabled="loading">
            <i class="fas fa-save"></i> {{ loading ? 'Salvando...' : 'Salvar Endereço' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  aberto:   Boolean,
  endereco: { type: Object, default: null }
})
const emit = defineEmits(['fechar', 'salvo'])

const loading  = ref(false)
const editando = ref(false)

const form = ref(formVazio())

function formVazio() {
  return { cep: '', endereco: '', numero: '', complemento: '', bairro: '', cidade: '', estado: '', pais: 'Brasil', principal: false }
}

watch(() => props.endereco, (e) => {
  if (e) { form.value = { ...formVazio(), ...e, principal: e.principal === 'sim' }; editando.value = true }
  else    { form.value = formVazio(); editando.value = false }
}, { immediate: true })

async function buscarCEP() {
  const cep = form.value.cep.replace(/\D/g, '')
  if (cep.length !== 8) return
  try {
    const res  = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
    const data = await res.json()
    if (!data.erro) {
      form.value.endereco = data.logradouro
      form.value.bairro   = data.bairro
      form.value.cidade   = data.localidade
      form.value.estado   = data.uf
    }
  } catch {}
}

async function salvar() {
  loading.value = true
  emit('salvo', { ...form.value })
  loading.value = false
}

const ufs = [
  {v:'AC',l:'Acre'},{v:'AL',l:'Alagoas'},{v:'AP',l:'Amapá'},{v:'AM',l:'Amazonas'},
  {v:'BA',l:'Bahia'},{v:'CE',l:'Ceará'},{v:'DF',l:'Distrito Federal'},{v:'ES',l:'Espírito Santo'},
  {v:'GO',l:'Goiás'},{v:'MA',l:'Maranhão'},{v:'MT',l:'Mato Grosso'},{v:'MS',l:'Mato Grosso do Sul'},
  {v:'MG',l:'Minas Gerais'},{v:'PA',l:'Pará'},{v:'PB',l:'Paraíba'},{v:'PR',l:'Paraná'},
  {v:'PE',l:'Pernambuco'},{v:'PI',l:'Piauí'},{v:'RJ',l:'Rio de Janeiro'},{v:'RN',l:'Rio Grande do Norte'},
  {v:'RS',l:'Rio Grande do Sul'},{v:'RO',l:'Rondônia'},{v:'RR',l:'Roraima'},{v:'SC',l:'Santa Catarina'},
  {v:'SP',l:'São Paulo'},{v:'SE',l:'Sergipe'},{v:'TO',l:'Tocantins'}
]
</script>
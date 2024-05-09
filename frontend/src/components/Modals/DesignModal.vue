<template>
  <Dialog
    v-model="show"
    :options="{
      size: '4xl',
      title: __('Create Design'),
    }"
  >
    <template #body-content>
      <div class="mb-4 grid grid-cols-1 ">
        <div class="flex items-center gap-3 text-sm text-gray-600">
          <!-- <div>{{ __('DTTHZ2N') }}</div>
          <Switch v-model="dtthz2n" />
        </div>
        <div class="flex items-center gap-3 text-sm text-gray-600">
          <div>{{ __('RGB') }}</div>
          <Switch v-model="rgb" />
        </div> -->
        <div>{{ __('Select Design Type') }}</div>
        <!-- <select v-model="selectedDesignType">
            <option value=""></option>
            <option value="DTTHZ2N">DTTHZ2N</option>
            <option value="RGB">RGB</option>
          </select> -->
          <FormControl
                type="select"
                :options="[
                  {
                    label: '',
                    value: '',
                  },
                  {
                    label: 'DTTHZ2N',
                    value: 'DTTHZ2N',
                  },
                  {
                    label: 'RGB',
                    value: 'RGB',
                  },
                ]"
                size="150px"
                placeholder=""
                :disabled="false"
                label=""
                v-model="selectedDesignType"
              />
          
        </div>
      </div>
      <Fields class="border-t pt-4" :sections="sections" :data="deal" />
      <ErrorMessage class="mt-4" v-if="error" :message="__(error)" />
    </template>
    <template #actions>
      <div class="flex flex-row-reverse gap-2">
        <Button
          variant="solid"
          :label="__('Create')"
          :loading="isDealCreating"
          @click="createDesign"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import Fields from '@/components/Fields.vue'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { Switch, createResource,Dropdown } from 'frappe-ui'
import { computed, ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const { getUser } = usersStore()
const { getDealStatus, statusOptions } = statusesStore()

const show = defineModel()
const router = useRouter()
const error = ref(null)

const deal = reactive({
  power_kva: '',
  hv_kv: '',
  hv_um_kv: '',
  hv_ac_kv: '',
  lv_v: '',
  lv_um_kv: '',
  lv_ac_kv: '',
  vectar_group: '',
  lv_li_kv: '',
  tappings_number_of_tappings: '',
  tappings_value: '',
  po_w: '',
  pk_w: '',
  uk: '',
  temperature_rise_k: '',
  ambient_max_temperature: '',
  transformer_ip: '',
  climatic_class: '',
  environment_class:'',
  lwa_db: '',
  lpa_db: '',
  thdi: '',
  parallel_coil: '',
  electrostatic_screen: '',
  special_parameters: ''
})

const isDealCreating = ref(false)
// const dtthz2n = ref(false)
// const rgb = ref(false)
const selectedDesignType = ref('')

const sections = computed(() => {
  let fields = []
  if (selectedDesignType.value === 'DTTHZ2N') {
    fields.push({
      section: 'DTTHZ2N',
      fields: [
      {
          label: 'HV (KV)',
          name: 'hv_kv',
          type: 'range',
          id: 'hv_kv_id',
          max:"100",
          step:"1",
          min:"0",
          placeholder: '',
        },
        {
          label: 'LV (V)',
          name: 'lv_v',
          type: 'range',
          id: 'lv_v_id',
          max:"120",
          step:"1",
          min:"0",
          placeholder: '',
        },
        {
          label: 'Vectar Group',
          name: 'vectar_group',
          type: 'int',
          placeholder: '',
         
        },
        {
          label: 'Power (KVA)',
          name: 'power_kva',
          type: 'int',
          placeholder: '',
        },
       
        {
          label: 'HV Um (kv)',
          name: 'hv_um_kv',
          type: 'select',
          options: [
            { label: __('1-10'), value: '1-10' },
            { label: __('11-50'), value: '11-50' },
            { label: __('51-200'), value: '51-200' },
            { label: __('201-500'), value: '201-500' },
            { label: __('501-1000'), value: '501-1000' },
            { label: __('1001-5000'), value: '1001-5000' },
            { label: __('5001-10000'), value: '5001-10000' },
            { label: __('10001+'), value: '10001+' },
          ],
          placeholder: '1-10',
        },
        {
          label: 'HV AC (KV)',
          name: 'hv_ac_kv',
          type: 'select',
          options: [
            { label: __('1-10'), value: '1-10' },
            { label: __('11-50'), value: '11-50' },
            { label: __('51-200'), value: '51-200' },
            { label: __('201-500'), value: '201-500' },
            { label: __('501-1000'), value: '501-1000' },
            { label: __('1001-5000'), value: '1001-5000' },
            { label: __('5001-10000'), value: '5001-10000' },
            { label: __('10001+'), value: '10001+' },
          ],
          placeholder: '1-10',
        },
        {
          label: 'LV Um (KV)',
          name: 'lv_um_kv',
          type: 'select',
          options: [
            { label: __('1-10'), value: '1-10' },
            { label: __('11-50'), value: '11-50' },
            { label: __('51-200'), value: '51-200' },
            { label: __('201-500'), value: '201-500' },
            { label: __('501-1000'), value: '501-1000' },
            { label: __('1001-5000'), value: '1001-5000' },
            { label: __('5001-10000'), value: '5001-10000' },
            { label: __('10001+'), value: '10001+' },
          ],
          placeholder: '1-10',
        },
        {
          label: 'LV AC (KV)',
          name: 'lv_ac_kv',
          type: 'select',
          options: [
            { label: __('1-10'), value: '1-10' },
            { label: __('11-50'), value: '11-50' },
            { label: __('51-200'), value: '51-200' },
            { label: __('201-500'), value: '201-500' },
            { label: __('501-1000'), value: '501-1000' },
            { label: __('1001-5000'), value: '1001-5000' },
            { label: __('5001-10000'), value: '5001-10000' },
            { label: __('10001+'), value: '10001+' },
          ],
          placeholder: '1-10',
        },
        {
          label: 'LV LI (KV)',
          name: 'lv_li_kv',
          type: 'int',
          placeholder: '',
        },
        {
          label: 'Tappings Number Of Tappings',
          name: 'tappings_number_of_tappings',
          type: 'int',
          placeholder: '',
        },
        {
          label: 'Tappings value',
          name: 'tappings_value',
          type: 'int',
          placeholder: '',
        },
      ],
    })
   } 
  else if (selectedDesignType.value === 'RGB') {
    fields.push({
      section: 'RGB',
      fields: [
        {
          label: 'PO (W)',
          name: 'po_w',
          type: 'link',
          placeholder: '',
          doctype: 'Contact',
        },
        {
          label: 'PK (W)',
          name: 'pk_w',
          type: 'link',
          doctype: 'Salutation',
          placeholder: '',
        },
        {
          label: 'UK',
          name: 'uk',
          type: 'data',
          placeholder: '',
        },
        {
          label: 'Temperature Rise (k)',
          name: 'temperature_rise_k',
          type: 'data',
          placeholder: '',
        },
        {
          label: 'Ambient Max Temperature',
          name: 'ambient_max_temperature',
          type: 'data',
          placeholder: '',
        },
        {
          label: 'Transfer IP',
          name: 'transformer_ip',
          type: 'int',
          placeholder: '',
        },
        {
          label: 'Climatic Class',
          name: 'climatic_class',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'Environment Class',
          name: 'environment_class',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'LWA (Db)',
          name: 'lwa_db',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'Lpa (Db)',
          name: 'lpa_db',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'THDI',
          name: 'thdi',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'Parallel Coil',
          name: 'parallel_coil',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
      ],
    })
  } 
  fields.push({
    section: '',
    columns: 2,
    fields: [
    {
          label: 'Electrostatic Screen',
          name: 'electrostatic_screen',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
        {
          label: 'Special Parameters',
          name: 'special_parameters',
          type: 'link',
          doctype: 'Gender',
          placeholder: '',
        },
    ],
  })
  return fields
})

const dealStatuses = computed(() => {
  let statuses = statusOptions('deal')
  if (!deal.status) {
    deal.status = statuses[0].value
  }
  return statuses
})

function createDesign() {
  createResource({
    url: 'crm.fcrm.doctype.crm_deal.crm_deal.create_deal',
    params: { args: deal },
    auto: true,
    validate() {
      error.value = null
      if (deal.website && !deal.website.startsWith('http')) {
        deal.website = 'https://' + deal.website
      }
      if (deal.annual_revenue) {
        deal.annual_revenue = deal.annual_revenue.replace(/,/g, '')
        if (isNaN(deal.annual_revenue)) {
          error.value = __('Annual Revenue should be a number')
          return error.value
        }
      }
      if (deal.mobile_no && isNaN(deal.mobile_no.replace(/[-+() ]/g, ''))) {
        error.value = __('Mobile No should be a number')
        return error.value
      }
      if (deal.email && !deal.email.includes('@')) {
        error.value = __('Invalid Email')
        return error.value
      }
      isDealCreating.value = true
    },
    onSuccess(name) {
      isDealCreating.value = false
      show.value = false
      router.push({ name: 'Deal', params: { dealId: name } })
    },
  })
}

onMounted(() => {
  if (!deal.deal_owner) {
    deal.deal_owner = getUser().email
  }
})
</script>

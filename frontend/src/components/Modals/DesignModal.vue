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
          <!-- <div class="rounded-md overflow-hidden" style="width: 200px;">
          <FormControl
            type="select"
            class="design-selector"
            :options="[
              { label: '', value: '' },
              { label: 'DTTHZ2N', value: 'DTTHZ2N' },
              { label: 'RGB', value: 'RGB' },
            ]"
            size="200px"
            placeholder=""
            :disabled="false"
            label=""
            v-model="selectedDesignType"
          />
        </div> -->
       
        <Select
          :options="transformerTypeOptions"
          v-model="selectedDesignType"
          style="width: 200px;" 
          
  />
         
        </div>
      </div>
      <Fields class="border-t pt-4" :sections="sections" :data="design" />
      <ErrorMessage class="mt-4" v-if="error" :message="__(error)" />
    </template>
    <template #actions>
      <div class="flex flex-row-reverse gap-2">
        <Button
          variant="solid"
          :label="__('Create')"
          :loading="isDesignCreating"
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
import { Switch, createResource,Dropdown, Select } from 'frappe-ui'
import { computed, ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'

const { getUser } = usersStore()
const { getDesignStatus, statusOptions } = statusesStore()

const show = defineModel()
const router = useRouter()
const error = ref(null)

const design = reactive({
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

// const designOptions = [
//   { label: '', value: '' },
//   { label: 'DTTHZ2N', value: 'DTTHZ2N' },
//   { label: 'RGB', value: 'RGB' },
// ];

// const handleDesignTypeChange = (value) => {
//   selectedDesignType.value = value;
// };

const isDesignCreating = ref(false)
// const dtthz2n = ref(false)
// const rgb = ref(false)
const selectedDesignType = ref('')
const transformerTypeOptions = ref([])

const sections = computed(() => {
  let fields = []
  if (selectedDesignType.value) {
    fetchTransformerDetails(selectedDesignType.value)
      .then((fetchedFields) => {
       console.log("push:",fetchedFields)
        if (fetchedFields) {
          fields.push({
            section: '',
            fields: fetchedFields
          });
        }
      })
      .catch((error) => {
        console.error('Error fetching transformer details:', error);
      });
  }
  // Push common fields outside the conditional block if needed
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
  });
  return fields
})

const designStatuses = computed(() => {
  let statuses = statusOptions('design')
  if (!design.status) {
    design.status = statuses[0].value
  }
  return statuses
})

async function fetchTransformerTypes() {
  try {
    const  message  = await call('crm.fcrm.doctype.design.api.get_item_variant');
    transformerTypeOptions.value = message;
   
  } catch (error) {
    console.error('Error fetching transformer types:', error);
  }
}



async function fetchTransformerDetails(transformerType) {
  try {
    const itemDetail = await call('frappe.client.get', {
      doctype: 'Item',
      name: transformerType
    });

    if (itemDetail.attributes) {
      const itemAttribute = itemDetail.attributes;
      const fields = []; // Declare fields variable here
      const attributeDetail = itemAttribute.map(async (attribute) => {
        const itemVariant = await call('frappe.client.get', {
          doctype: 'Item Attribute',
          name: attribute.attribute
        });
       
        let field;
        if (itemVariant.numeric_values != 1) {
          // If numeric_value is 0, it should be a select type
          field = {
            label: itemVariant.attribute_name,
            name: itemVariant.attribute_name.replace(/\s+/g, '_').replace(/[()]/g, '').toLowerCase(),
            type: 'select',
            options: itemVariant.item_attribute_values.map(val => ({
              label: val.abbr,
              value: val.attribute_value
            }))
          };
        } else {
          // Otherwise, it's an integer type
          field = {
            label: itemVariant.attribute_name,
            name: itemVariant.attribute_name.replace(/\s+/g, '_').replace(/[()]/g, '').toLowerCase(),
            type: 'int',
            placeholder: ''
          };
        }
        return field;
      });

      const fetchedFields = await Promise.all(attributeDetail);
      console.log('Fields:', fetchedFields);
      return fetchedFields;
    }
  } catch (error) {
    console.error('Error fetching transformer details:', error);
  }
}






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
      isDesignCreating.value = true
    },
    onSuccess(name) {
      isDesignCreating.value = false
      show.value = false
      router.push({ name: 'Design', params: { designId: name } })
    },
  })
}

onMounted(() => {
  if (!design.design_owner) {
    design.design_owner = getUser().email
  }
  fetchTransformerTypes()
})

watch(() => selectedDesignType.value, (newValue, oldValue) => {
  if(newValue !== oldValue) {
    fetchTransformerDetails(newValue);
  }
});


</script>
<style scoped>
/* Remove outline for the specific formControl component */
.form-control:focus,
.form-control:focus-visible {
  outline: none !important;
}
</style>
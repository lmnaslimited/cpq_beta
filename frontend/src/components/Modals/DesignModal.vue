<template>
  <Dialog
    v-model="show"
    :options="{
      size: '4xl',
      title: __('Create Design'),
    }"
  >
    <template #body-content>
      <div class="mb-4 grid grid-cols-1">
        <div class="flex items-center gap-3 text-sm text-gray-600">
          <div>{{ __('Select Design Type') }}</div>
          <Select
            :options="transformerTypeOptions"
            v-model="design.design_type"
            style="width: 200px;"
          />
        </div>
      </div>
      <Fields class="border-t pt-4" :sections="sections" :data="design" @updateField="handleFieldUpdate" />
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
import { Select } from 'frappe-ui'
import { computed, ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { call } from 'frappe-ui'

const { getUser } = usersStore()
const { getDesignStatus, statusOptions } = statusesStore()

const show = defineModel()
const router = useRouter()
const error = ref(null)

const design = reactive({
  design_owner: '',
   design_type: '',
   rating: '',
})

const isDesignCreating = ref(false)
const transformerTypeOptions = ref([])
const fetchedFields = ref([])

const sections = computed(() => {
  const fields = fetchedFields.value.length ? [{
    section: '',
    fields: fetchedFields.value
  }] : []

  fields.push({
    section: '',
    columns: 2,
    fields: [
      {
        label: 'Rating',
        name: 'rating',
        type: 'data',
        placeholder: '',
      },
    ],
  })
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
    const message = await call('crm.fcrm.doctype.design.api.get_item_variant')
    transformerTypeOptions.value = message
  } catch (error) {
    console.error('Error fetching transformer types:', error)
  }
}

async function fetchTransformerDetails(transformerType) {
  try {
    const itemDetail = await call('frappe.client.get', {
      doctype: 'Item',
      name: transformerType
    })

    if (itemDetail.attributes) {
      const itemAttribute = itemDetail.attributes
      const fields = await Promise.all(itemAttribute.map(async (attribute) => {
        const itemVariant = await call('frappe.client.get', {
          doctype: 'Item Attribute',
          name: attribute.attribute
        })

        let field
        if (itemVariant.numeric_values != 1) {
          // If numeric_value is 0, it should be a select type
          field = {
            label: itemVariant.attribute_name,
            name: itemVariant.attribute_name.replace(/\s+/g, '_').replace(/[()]/g, '').toLowerCase(),
            type: 'select',
            options: itemVariant.item_attribute_values.map(val => ({
              label: val.attribute_value,
              value: val.attribute_value
            }))
          }
        } else {
          // Otherwise, it's an range type
          field = {
            label: itemVariant.attribute_name,
            name: itemVariant.attribute_name.replace(/\s+/g, '_').replace(/[()]/g, '').toLowerCase(),
            type: 'range',
            min: itemVariant.from_range,
            max: itemVariant.to_range,
            step: itemVariant.increment,
            id: `${itemVariant.attribute_name.replace(/\s+/g, '_').replace(/[()]/g, '').toLowerCase()}_id`,
            placeholder: ''
          }
        }
        return field
      }))
      fetchedFields.value = fields
    }
  } catch (error) {
    console.error('Error fetching transformer details:', error)
  }
}

async function createDesign() {
  isDesignCreating.value = true
  error.value = null

  try {
    // Prepare the data payload
    const payload = {}

    // Include fields from fetchedFields
    for (const [key, value] of Object.entries(design)) {
      const field = fetchedFields.value.find(field => field.name === key)

      if (field) {
        payload[field.label] = {
          label: field.label,
          name: field.name,
          value: value,
          type: 'data'
        }
      }
    }

    // Include other fields like design_owner and design_type
    payload['Design Owner'] = {
      label: 'Design Owner',
      name: 'design_owner',
      value: design.design_owner,
      type: 'data'
    };

    payload['Design Type'] = {
      label: 'Design Type',
      name: 'design_type',
      value: design.design_type,
      type: 'data'
    };

    // Include the "Rating" field
    const ratingField = {
      label: 'Rating',
      name: 'rating',
      value: design.rating,
      type: 'data'
    };

    // Add the "Rating" field to the payload
    payload['Rating'] = ratingField;

    const response = await call('crm.fcrm.doctype.design.api.save_design', {
      data: payload
    })

    if (response.status === 'success') {
      isDesignCreating.value = false
      show.value = false
      router.push({ name: 'Design', params: { designId: response.docname } })
    } else {
      error.value = response.message
    }
  } catch (err) {
    error.value = err.message
  } finally {
    isDesignCreating.value = false
  }
}




function handleFieldUpdate({ name, value }) {
  design[name] = value
}

onMounted(() => {
  if (!design.design_owner) {
    design.design_owner = getUser().email
  }
  fetchTransformerTypes()
})

watch(() => design.design_type, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    fetchTransformerDetails(newValue)
  }
})
</script>

<style scoped>
/* Remove outline for the specific formControl component */
.form-control:focus,
.form-control:focus-visible {
  outline: none !important;
}
</style>

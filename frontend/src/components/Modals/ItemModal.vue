<template>
    <Dialog
      v-model="show"
      :options="{
        size: '2xl',
        title: __('Create Item'),
      }"
    >
      <template #body-content>
        <Fields :sections="sections" :data="item" />
        <ErrorMessage class="mt-4" v-if="error" :message="__(error)" />
      </template>
      <template #actions>
        <div class="flex flex-row-reverse gap-2">
          <Button
            variant="solid"
            :label="__('Create')"
            :loading="isItemCreating"
            @click="createNewItem"
          />
        </div>
      </template>
    </Dialog>
  </template>
  
  <script setup>
  import Fields from '@/components/Fields.vue'
  import { usersStore } from '@/stores/users'
  import { statusesStore } from '@/stores/statuses'
  import { createResource } from 'frappe-ui'
  import { computed, onMounted, ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  
  const { getUser } = usersStore()
  const { getLeadStatus, statusOptions } = statusesStore()
  
  const show = defineModel()
  const router = useRouter()
  const error = ref(null)
  const isItemCreating = ref(false)
  
  const item = reactive({
    item_code: '',
    item_name: '',
    item_group: '',
    standard_rate: '',
    uom: 'Nos',
    description: ''
    
  })
  
  const sections = computed(() => {
    return [
      {
        section: '',
        columns: '2',
        fields: [
          {
            label: 'Item Name',
            name: 'item_name',
            type: 'data',
            placeholder: 'Item Name',
            mandatory: true
            
          },
          {
            label: 'Item code',
            name: 'item_code',
            type: 'data',
            placeholder: 'Item Code',
            mandatory: true
            
          },
          {
            label: 'Item Group',
            name: 'item_group',
            type: 'link',
            placeholder: 'Item Group',
            doctype: 'Item Group',
            mandatory: true
          },
          {
            label: 'Standard Selling Rate',
            name: 'standard_rate',
            type: 'data',
            placeholder: '99,999',
            
          },
          {
            label: 'Unit of Measure (UoM)',
            name: 'uom',
            type: 'link',
            placeholder: '',
            doctype: 'UOM',
          },
         
         
        ],
      },
      {
        section: '',
        columns: '1',
        fields:[
        {
            label: 'Description',
            name: 'description',
            type: 'textbox',
            placeholder: 'Description',
            
          },
        ]
      }
      
    ]
  })
  
  const createItem = createResource({
    url: 'frappe.client.insert',
    makeParams(values) {
      return {
        doc: {
          doctype: 'Item',
          ...values,
        },
      }
    },
  })
  

  
  function createNewItem() {
    createItem.submit(item, {
      validate() {
        error.value = null
        
        if (item.standard_rate) {
          item.standard_rate = item.standard_rate.replace(/,/g, '')
          if (isNaN(item.standard_rate)) {
            error.value = __('Standard Selling Rate should be a number')
            return error.value
          }
        }
        
        isItemCreating.value = true
      },
      onSuccess(data) {
        isItemCreating.value = false
        show.value = false
        router.push({ name: 'Item', params: { itemId: data.name } })
      },
    })
  }
  

  </script>
  
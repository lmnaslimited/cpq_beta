<template>
  <div v-if="item?.data" class="flex h-full overflow-hidden">
    <Tabs v-model="tabIndex" :tabs="tabs">
      <template #default="{ tab }">
        <Activities
          v-if="tabIndex === tabs.findIndex(t => t.name === tab.name)"
          ref="activities"
          doctype="Item"
          :title="tab.name"
          v-model:reload="reload"
          v-model="item"
        />
      </template>
    </Tabs>
    <div class="flex w-[352px] flex-col justify-between border-l">
      <div class="flex h-10.5 items-center border-b px-5 py-2.5 text-lg font-semibold">
        {{ __('About this item') }}
      </div>
      <FileUploader @success="(file) => updateField('image', file.file_url)" :validateFile="validateFile">
        <template #default="{ openFileSelector, error }">
          <div class="flex items-center justify-start gap-5 border-b p-5">
            <div class="group relative h-[88px] w-[88px]">
              <Avatar size="3xl" class="h-[88px] w-[88px]" :label="item.data.name" :image="item.data.image" />
              <component
                :is="item.data.image ? 'Dropdown' : 'div'"
                v-bind="item.data.image ? {
                  options: [
                    {
                      icon: 'upload',
                      label: item.data.image ? __('Change image') : __('Upload image'),
                      onClick: openFileSelector,
                    },
                    {
                      icon: 'trash-2',
                      label: __('Remove image'),
                      onClick: () => updateField('image', ''),
                    },
                  ],
                } : { onClick: openFileSelector }"
                class="!absolute bottom-0 left-0 right-0"
              >
                <div
                  class="z-1 absolute bottom-0 left-0 right-0 flex h-13 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-3 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                  style="-webkit-clip-path: inset(12px 0 0 0); clip-path: inset(12px 0 0 0);"
                >
                  <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
                </div>
              </component>
            </div>
            <div class="flex flex-col gap-2.5 truncate">
              <Tooltip :text="item.data.name">
                <div class="truncate text-2xl font-medium">{{ item.data.name }}</div>
              </Tooltip>
              <!-- <div class="flex gap-1.5">Add additional details here if needed</div> -->
              <ErrorMessage :message="__(error)" />
            </div>
          </div>
        </template>
      </FileUploader>
      <div v-if="detailSections.length" class="flex flex-1 flex-col justify-between overflow-hidden mt-4">
        <div class="flex flex-col overflow-y-auto">
          <div v-for="(section, i) in detailSections" :key="section.label" class="flex flex-col p-5" :class="{ 'border-b': i !== detailSections.length - 1 }">
            <Section :is-opened="section.opened" :label="section.label">
              <div v-if="section.label === 'Details'" class="mt-4 space-y-2">
                <div class="text-s ml-4"><span class="font-semibold">{{ __('Item Code') }}:</span> {{ item.data.item_code }}</div>
                <div class="text-s ml-4"><span class="font-semibold">{{ __('Item Group') }}:</span> {{ item.data.item_group }}</div>
                <div class="text-s ml-4"><span class="font-semibold">{{ __('Name') }}:</span> {{ item.data.name }}</div>
                <div class="text-s ml-4"><span class="font-semibold">{{ __('Description') }}:</span> {{ item.data.description }}</div>
              </div>
              <div v-else-if="section.label === 'Variants'" class="mt-4 space-y-2">
                <div v-for="(variant, index) in variantAttributes" :key="index" class="text-s ml-4">
                  <span class="font-semibold">{{ variant.attribute }}:</span> {{ variant.attribute_value }}
                </div>
              </div>
              <SectionFields v-else :fields="section.fields" v-model="item.data" @update="updateField" />
            </Section>
          </div>
        </div>
      </div>
    </div>
    <AssignmentModal v-if="item.data" :doc="item.data" v-model="showAssignmentModal" v-model:assignees="item.data._assignedTo" />
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import LinkIcon from '@/components/Icons/LinkIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import Activities from '@/components/Activities.vue'
import AssignmentModal from '@/components/Modals/AssignmentModal.vue'
import MultipleAvatar from '@/components/MultipleAvatar.vue'
import Section from '@/components/Section.vue'
import SectionFields from '@/components/SectionFields.vue'
import { createResource, FileUploader, Tooltip, Avatar, Tabs } from 'frappe-ui'
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { globalStore } from '@/stores/global'
import { contactsStore } from '@/stores/contacts'
import { organizationsStore } from '@/stores/organizations'
import { statusesStore } from '@/stores/statuses'

const { $dialog, makeCall } = globalStore()
const { getContactByName, contacts } = contactsStore()
const { organizations } = organizationsStore()
const { statusOptions, getLeadStatus } = statusesStore()
const router = useRouter()

const props = defineProps({
  itemId: {
    type: String,
    required: true,
  },
})

const item = createResource({
  url: 'crm.fcrm.doctype.item.api.get_item',
  params: { name: props.itemId },
  cache: ['item', props.itemId],
  onSuccess: (data) => {
    setupAssignees(data)
    setupCustomActions(data, {
      doc: data,
      $dialog,
      router,
      updateField,
      createToast,
    })
  },
})

onMounted(() => {
  if (item.data) return
  item.fetch()
})

const reload = ref(false)
const showAssignmentModal = ref(false)

const breadcrumbs = computed(() => [
  { label: 'Items', to: { name: 'Items' } },
  { label: item.data?.name },
])

const tabIndex = ref(0)
const tabs = [
  { name: 'Activity', label: __('Activity'), icon: ActivityIcon },
  { name: 'Emails', label: __('Emails'), icon: EmailIcon },
  { name: 'Calls', label: __('Calls'), icon: PhoneIcon },
  { name: 'Tasks', label: __('Tasks'), icon: TaskIcon },
  { name: 'Notes', label: __('Notes'), icon: NoteIcon },
  { name: 'Prices', label: __('Prices'), icon: TaskIcon },
  // { name: 'Variants', label: __('Variants'), icon: TaskIcon },
  
]

const variantAttributes = computed(() => {
  return item.data?.variant_attributes || []
})

function validateFile(file) {
  let extn = file.name.split('.').pop().toLowerCase()
  if (!['png', 'jpg', 'jpeg'].includes(extn)) {
    return __('Only PNG and JPG images are allowed')
  }
}

const detailSections = computed(() => {
  let data = item.data
  if (!data) return []
  return data.doctype_fields.filter(
    (section) => section.label === 'Details' || section.label === 'Variants'
  )
})

function updateField(name, value, callback) {
  createResource({
    url: 'frappe.client.set_value',
    params: {
      doctype: 'Item',
      name: props.itemId,
      fieldname: name,
      value,
    },
    auto: true,
    onSuccess: () => {
      item.reload()
      reload.value = true
      callback?.()
    },
  })
}
</script>

<style scoped>
/* Add your scoped styles here */
</style>

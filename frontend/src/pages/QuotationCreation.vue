<template>
<LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="quotationsListView?.customListActions"
        :actions="quotationsListView.customListActions"
      />
    </template>
  </LayoutHeader>
  <!-- <Tabs v-model="tabIndex" :tabs="tabs">
        <template #default="{ tab }">
          <Activities
            v-if="tabIndex === tabs.findIndex(t => t.name === tab.name)"
            ref="activities"
            doctype="Quotation"
            :title="tab.name"
            v-model:reload="reload"
            v-model="quotation"
          />
        </template>
      </Tabs> -->
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs } from 'frappe-ui'
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
  import { createResource, FileUploader, Tooltip, Avatar, Tabs } from 'frappe-ui'
  import { ref } from 'vue'


  const props = defineProps({
    quotationId: {
      type: String,
      required: true,
    },
  })
const breadcrumbs = [{ label: __('Offer Creation'), route: { name: 'QuotationCreation' } }]

const tabIndex = ref(0)
  const tabs = [
    { name: 'Activity', label: __('Activity'), icon: ActivityIcon },
    { name: 'Emails', label: __('Emails'), icon: EmailIcon },
    { name: 'Calls', label: __('Calls'), icon: PhoneIcon },
    { name: 'Tasks', label: __('Tasks'), icon: TaskIcon },
    { name: 'Notes', label: __('Notes'), icon: NoteIcon },
    { name: 'Prices', label: __('Prices'), icon: TaskIcon },
  ]

  const quotation = createResource({
    url: 'crm.fcrm.doctype.quotation.api.get_quotation',
    params: { name: props.quotationId },
    cache: ['quotation', props.quotationId],
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

</script>
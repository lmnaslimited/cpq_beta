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
      <Button
        variant="solid"
        :label="__('Create')"
         @click="handleClick"
      >
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="quotations"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Quotation"
  />
  <QuotationsListView
    ref="quotationsListView"
    v-if="quotations.data && rows.length"
    v-model="quotations.data.page_length_count"
    v-model:list="quotations"
    :rows="rows"
    :columns="quotations.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: quotations.data.row_count,
      totalCount: quotations.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
  />
  <div v-else-if="quotations.data" class="flex h-full items-center justify-center">
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500"
    >
      <DealsIcon class="h-10 w-10" />
      <span>{{ __('No Quotations Found') }}</span>
      <Button :label="__('Create')" @click="showDesignModal = true">
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </div>
  </div>
  <DesignModal v-model="showDesignModal" />

</template>

<script setup>

import CustomActions from '@/components/CustomActions.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewControls from '@/components/ViewControls.vue'
import QuotationsListView from '@/components/ListViews/QuotationsListView.vue'
import DesignModal from '@/components/Modals/DesignModal.vue'
import { usersStore } from '@/stores/users'
import { organizationsStore } from '@/stores/organizations'
import { useRouter } from 'vue-router'

import { statusesStore } from '@/stores/statuses'

import {
  dateFormat,
  dateTooltipFormat,
  timeAgo,
  formatNumberIntoCurrency,
  formatTime,
} from '@/utils'
import { Breadcrumbs } from 'frappe-ui'
import { ref, computed } from 'vue'


const breadcrumbs = [{ label: __('Quotations'), route: { name: 'Quotations' } }]
const { getUser } = usersStore()
const { getOrganization } = organizationsStore()
const { getDealStatus } = statusesStore()

const quotationsListView = ref(null)
const showDesignModal = ref(false)
const router = useRouter()

// desigs data is loaded in the ViewControls component
const quotations = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

function handleClick() {
    router.push({ name: 'QuotationCreation' })
}

// Rows
const rows = computed(() => {
  if (!quotations.value?.data?.data) return []
  return quotations.value.data.data.map((quotation) => {
    let _rows = {}
    quotations.value.data.rows.forEach((row) => {
      _rows[row] = quotation[row]
    })
    return _rows
  })
})
</script>
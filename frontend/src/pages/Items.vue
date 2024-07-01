<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="itemsListView?.customListActions"
        :actions="itemsListView.customListActions"
      />
      <Button
        variant="solid"
        :label="__('Create')"
        @click="showItemModal = true"
      >
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="items"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Item"
  />
  <ItemsListView
    ref="itemsListView"
    v-if="items.data && rows.length"
    v-model="items.data.page_length_count"
    v-model:list="items"
    :rows="rows"
    :columns="items.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: items.data.row_count,
      totalCount: items.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
  />
  <div v-else-if="items.data" class="flex h-full items-center justify-center">
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500"
    >
      <DealsIcon class="h-10 w-10" />
      <span>{{ __('No items Found') }}</span>
      <Button :label="__('Create')" @click="showItemModal = true">
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </div>
  </div>
  <ItemModal v-model="showItemModal" />
</template>

<script setup>

import CustomActions from '@/components/CustomActions.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewControls from '@/components/ViewControls.vue'
import ItemsListView from '@/components/ListViews/ItemsListView.vue'
// import ItemModal from '@/components/Modals/ItemModal.vue'
import { usersStore } from '@/stores/users'
import { organizationsStore } from '@/stores/organizations'

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


const breadcrumbs = [{ label: __('Items'), route: { name: 'Items' } }]
const { getUser } = usersStore()
const { getOrganization } = organizationsStore()
const { getDealStatus } = statusesStore()

const itemsListView = ref(null)
const showItemModal = ref(false)

// items data is loaded in the ViewControls component
const items = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

// Rows
const rows = computed(() => {
  if (!items.value?.data?.data) return []
  return items.value.data.data.map((item) => {
    //console.log(items.value.data)
    let _rows = {}
    items.value.data.rows.forEach((row) => {
      // /console.log(row)
      _rows[row] = item[row]
      // // console.log(_rows)
      // if (row == 'name') {
      //   _rows[row] = {
      //     label: item.name
      //   }
      // } else if (row == 'modified') {
      //   _rows[row] = {
         
      //   }
      // } 
    })
    //console.log(_rows)
    return _rows
   })
  
 })
//  console.log(rows)
</script>





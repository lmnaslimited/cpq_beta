<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="pricesListView?.customListActions"
        :actions="pricesListView.customListActions"
      />
      <Button variant="solid" :label="__('Create')" @click="createPrice">
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="prices"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Price"
  />
  <PricesListView
    ref="pricesListView"
    v-if="prices.data && rows.length"
    v-model="prices.data.page_length_count"
    v-model:list="prices"
    :rows="rows"
    :columns="prices.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: prices.data.row_count,
      totalCount: prices.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @showPrice="showPrice"
    @applyFilter="(data) => viewControls.applyFilter(data)"
  />
  <div v-else-if="prices.data" class="flex h-full items-center justify-center">
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500"
    >
      <EmailIcon class="h-10 w-10" />
      <span>{{ __('No Prices Found') }}</span>
      <Button :label="__('Create')" @click="showPriceModal = true">
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </div>
  </div>
  <PriceModal v-model="showPriceModal" v-model:reloadPrices="prices" :price="price" />
</template>

<script setup>
import CustomActions from '@/components/CustomActions.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewControls from '@/components/ViewControls.vue'
import PricesListView from '@/components/ListViews/PricesListView.vue'
import TaskModal from '@/components/Modals/TaskModal.vue'
import { usersStore } from '@/stores/users'
import { dateFormat, dateTooltipFormat, timeAgo } from '@/utils'
import { Breadcrumbs } from 'frappe-ui'
import { computed, ref } from 'vue'

const breadcrumbs = [{ label: __('Prices'), route: { name: 'Prices' } }]

const { getUser } = usersStore()

const PricesListView = ref(null)

// prices data is loaded in the ViewControls component
const prices = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const rows = computed(() => {
  if (!prices.value?.data?.data) return []
  return prices.value?.data.data.map((price) => {
    let _rows = {}
    prices.value?.data.rows.forEach((row) => {
      _rows[row] = price[row]

      if (['modified', 'creation'].includes(row)) {
        _rows[row] = {
          label: dateFormat(price[row], dateTooltipFormat),
          timeAgo: __(timeAgo(price[row])),
        }
      } else if (row == 'assigned_to') {
        _rows[row] = {
          label: price.assigned_to && getUser(price.assigned_to).full_name,
          ...(price.assigned_to && getUser(price.assigned_to)),
        }
      }
    })
    return _rows
  })
})

const showTaskModal = ref(false)

const price = ref({
  name: '',
  title: '',
  description: '',
  assigned_to: '',
  due_date: '',
  status: 'Backlog',
  priority: 'Low',
  reference_doctype: 'CRM Lead',
  reference_docname: '',
})

function showPrice(name) {
  let t = rows.value?.find((row) => row.name === name)
  price.value = {
    name: t.name,
    title: t.title,
    description: t.description,
    assigned_to: t.assigned_to?.email || '',
    due_date: t.due_date,
    status: t.status,
    priority: t.priority,
    reference_doctype: t.reference_doctype,
    reference_docname: t.reference_docname,
  }
  showTaskModal.value = true
}

function createPrice() {
  price.value = {
    name: '',
    title: '',
    description: '',
    assigned_to: '',
    due_date: '',
    status: 'Backlog',
    priority: 'Low',
    reference_doctype: 'CRM Lead',
    reference_docname: '',
  }
  showTaskModal.value = true
}
</script>

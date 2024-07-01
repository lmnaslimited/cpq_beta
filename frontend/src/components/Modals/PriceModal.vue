<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'xl',
      actions: [
        {
          label: editMode ? __('Update') : __('Create'),
          variant: 'solid',
          onClick: () => updateTask(),
        },
      ],
    }"
  >
    <template #body-title>
      <div class="flex items-center gap-3">
        <h3 class="text-2xl font-semibold leading-6 text-gray-900">
          {{ editMode ? __('Edit Task') : __('Create Task') }}
        </h3>
        <Button
          v-if="task?.reference_docname"
          variant="outline"
          size="sm"
          :label="
            task.reference_doctype == 'Item'
          "
          @click="redirect()"
        >
          <template #suffix>
            <ArrowUpRightIcon class="h-4 w-4" />
          </template>
        </Button>
      </div>
    </template>
    <template #body-content>
      <div class="flex flex-col gap-4">
        <div>
          <div class="mb-1.5 text-sm text-gray-600">{{ __('Price List') }}</div>
          <TextInput
            ref="title"
            variant="outline"
            v-model="_task.price_list"
            :placeholder="__('')"
          />
        </div>
        <div>
          <div class="mb-1.5 text-sm text-gray-600">{{ __('Price List Rate') }}</div>
          <TextEditor
            variant="outline"
            ref="description"
            editor-class="!prose-sm overflow-auto min-h-[80px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
            :bubbleMenu="true"
            :content="_price.price_list_rate"
            @change="(val) => (_price.price_list_rate = val)"
            :placeholder="__('')"
          />
        </div>
        <div class="flex items-center gap-2">
          <!-- <Dropdown :options="taskStatusOptions(updateTaskStatus)"> -->
            <!-- <Button :label="_task.status" class="w-full justify-between"> -->
              <!-- <template #prefix>
                <TaskStatusIcon :status="_task.status" />
              </template> -->
            <!-- </Button> -->
          <!-- </Dropdown> -->
          <!-- <Link
            class="form-control"
            :value="getUser(_task.assigned_to).full_name"
            doctype="User"
            @change="(option) => (_task.assigned_to = option)"
            :placeholder="__('John Doe')"
            :hideMe="true"
          > -->
            <!-- <template #prefix>
              <UserAvatar class="mr-2 !h-4 !w-4" :user="_task.assigned_to" />
            </template>
            <template #item-prefix="{ option }">
              <UserAvatar class="mr-2" :user="option.value" size="sm" />
            </template>
            <template #item-label="{ option }">
              <Tooltip :text="option.value">
                <div class="cursor-pointer">
                  {{ getUser(option.value).full_name }}
                </div>
              </Tooltip>
            </template> -->
          <!-- </Link> -->
          <DatetimePicker
            class="datepicker w-36"
            icon-left="calendar"
            :value="_task.due_date"
            @change="(val) => (_task.due_date = val)"
            :placeholder="__('01/04/2024 11:30 PM')"
            input-class="border-none"
          />
          <Dropdown :options="taskPriorityOptions(updateTaskPriority)">
            <Button :label="_task.priority" class="w-full justify-between">
              <template #prefix>
                <TaskPriorityIcon :priority="_task.priority" />
              </template>
            </Button>
          </Dropdown>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import TaskStatusIcon from '@/components/Icons/TaskStatusIcon.vue'
import TaskPriorityIcon from '@/components/Icons/TaskPriorityIcon.vue'
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Link from '@/components/Controls/Link.vue'
import { taskStatusOptions, taskPriorityOptions } from '@/utils'
import { usersStore } from '@/stores/users'
import DatetimePicker from '@/components/Controls/DatetimePicker.vue'
import { TextEditor, Dropdown, Tooltip, call } from 'frappe-ui'
import { ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  price: {
    type: Object,
    default: {},
  },
  doctype: {
    type: String,
    default: 'Item',
  },
  doc: {
    type: String,
    default: '',
  },
})

const show = defineModel()
const prices = defineModel('reloadPricess')

const emit = defineEmits(['updatePrice'])

const router = useRouter()
const { getUser } = usersStore()

const title = ref(null)
const editMode = ref(false)
const _price = ref({
	price_list: '',
	price_list_rate: '',
	currency: '',
  reference_doctype: props.doctype,
  reference_docname: null,
})

// function updateTaskStatus(status) {
//   _task.value.status = status
// }

// function updateTaskPriority(priority) {
//   _task.value.priority = priority
// }

function redirect() {
  if (!props.price?.reference_docname) return
  let name = props.price.reference_doctype == 'CRM Deal' ? 'Deal' : 'Lead'
  let params = { leadId: props.price.reference_docname }
  if (name == 'Deal') {
    params = { dealId: props.price.reference_docname }
  }
  router.push({ name: name, params: params })
}

async function updatePrice() {
  if (!_price.value.assigned_to) {
    _price.value.assigned_to = getUser().email
  }
  if (_price.value.name) {
    let d = await call('frappe.client.set_value', {
      doctype: 'Item price',
      name: _price.value.name,
      fieldname: _price.value,
    })
    if (d.name) {
      prices.value.reload()
    }
  } else {
    let d = await call('frappe.client.insert', {
      doc: {
        doctype: 'Item Price',
        reference_doctype: props.doctype,
        reference_docname: props.doc || null,
        ..._price.value,
      },
    })
    if (d.name) {
      prices.value.reload()
    }
  }
  show.value = false
}

watch(
  () => show.value,
  (value) => {
    if (!value) return
    editMode.value = false
    nextTick(() => {
      title.value.el.focus()
      _price.value = { ...props.price }
      if (_price.value.title) {
        editMode.value = true
      }
    })
  }
)
</script>

<style scoped>
:deep(.datepicker svg) {
  width: 0.875rem;
  height: 0.875rem;
}
</style>

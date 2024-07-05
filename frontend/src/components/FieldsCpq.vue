<template>
    <div class="flex flex-col gap-4">
      <div
        v-for="section in sections"
        :key="section.label"
        class="first:border-t-0 first:pt-0"
        :class="section.hideBorder ? '' : 'border-t pt-4'"
      >
        <div
          v-if="!section.hideLabel"
          class="flex h-7 mb-3 max-w-fit cursor-pointer items-center gap-2 text-base font-semibold leading-5"
        >
          {{ section.label }}
        </div>
        <div
          class="grid gap-4"
          :class="
            section.columns
              ? 'grid-cols-' + section.columns
              : 'grid-cols-2 sm:grid-cols-3'
          "
        >
          <div v-for="field in section.fields" :key="field.name">
            <div
              v-if="
                field.type == 'Check' ||
                (field.read_only && data[field.name]) ||
                !field.read_only || !field.hidden
              "
            >
              <div
                v-if="field.type != 'Check'"
                class="mb-2 text-sm text-gray-600"
              >
                {{ __(field.label) }}
                <span class="text-red-500" v-if="field.mandatory">*</span>
              </div>
              <FormControl
                v-if="field.read_only && field.type !== 'Check'"
                type="text"
                :placeholder="__(field.placeholder || field.label)"
                v-model="data[field.name]"
                :disabled="true"
              />
              <FormControl
                v-else-if="field.type === 'Select'"
                type="select"
                class="form-control"
                :class="field.prefix ? 'prefix' : ''"
                :options="field.options"
                v-model="data[field.name]"
                :placeholder="__(field.placeholder || field.label)"
              >
                <template v-if="field.prefix" #prefix>
                  <IndicatorIcon :class="field.prefix" />
                </template>
              </FormControl>
              <div
                v-else-if="field.type == 'Check'"
                class="flex items-center gap-2"
              >
                <FormControl
                  class="form-control"
                  type="checkbox"
                  v-model="data[field.name]"
                  @change="(e) => (data[field.name] = e.target.checked)"
                  :disabled="Boolean(field.read_only)"
                />
                <label
                  class="text-sm text-gray-600"
                  @click="data[field.name] = !data[field.name]"
                >
                  {{ __(field.label) }}
                  <span class="text-red-500" v-if="field.mandatory">*</span>
                </label>
              </div>
              <Link
                v-else-if="field.type === 'Link'"
                class="form-control"
                :value="data[field.name]"
                :doctype="field.options"
                @change="(v) => (data[field.name] = v)"
                :placeholder="__(field.placeholder || field.label)"
                :onCreate="field.create"
              />
              <Link
                v-else-if="field.type === 'User'"
                class="form-control"
                :value="getUser(data[field.name]).full_name"
                :doctype="field.options"
                @change="(v) => (data[field.name] = v)"
                :placeholder="__(field.placeholder || field.label)"
                :hideMe="true"
              >
                <template #prefix>
                  <UserAvatar class="mr-2" :user="data[field.name]" size="sm" />
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
                </template>
              </Link>
              <!-- this is for extra fields used for Design Cpq -->
              <div v-else-if="field.type === 'Range'">
            <input
              type="range"
              :class="field.name"
              :min="field.min"
              :max="field.max"
              :step="field.step"
              v-model="data[field.name]"
              @input="updateRangeDisplay(field.name, $event.target.value)"
              @change="handleRangeChange(field.name, $event.target.value, field.min,field.max, field.step)"
              @blur="handleRangeChange(field.name, data[field.name], field.min,field.max, field.step)"
              style="width:250px; accent-color: black;"
              variant="ghost"
            />
            <p
              :id="field.name"
              class="text-gray-600 rounded px-2"
              contenteditable="true"
              @input="updateRangeValue(field.name, $event.target.innerText, field.min,field.max, field.step)"
              style="background-color: #f5f5f5;"
            >
              {{ data[field.name] }}
            </p>
            <span v-if="rangeErrors[field.name]" class="text-red-500">{{ rangeErrors[field.name] }}</span>
          </div> 
           <div v-else-if="field.type === 'textbox'">
            <FormControl
              :type="'textarea'"
              size="sm"
              variant="subtle"
              :placeholder="__(field.placeholder)"
              :disabled="false"
              v-model="inputValue"
            />
          </div>

              <div v-else-if="field.type === 'Dropdown'">
                <NestedPopover>
                  <template #target="{ open }">
                    <Button
                      :label="data[field.name]"
                      class="dropdown-button flex w-full items-center justify-between rounded border border-gray-100 bg-gray-100 px-2 py-1.5 text-base text-gray-800 placeholder-gray-500 transition-colors hover:border-gray-200 hover:bg-gray-200 focus:border-gray-500 focus:bg-white focus:shadow-sm focus:outline-none focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400"
                    >
                      <div class="truncate">{{ data[field.name] }}</div>
                      <template #suffix>
                        <FeatherIcon
                          :name="open ? 'chevron-up' : 'chevron-down'"
                          class="h-4 text-gray-600"
                        />
                      </template>
                    </Button>
                  </template>
                  <template #body>
                    <div
                      class="my-2 space-y-1.5 divide-y rounded-lg border border-gray-100 bg-white p-1.5 shadow-xl"
                    >
                      <div>
                        <DropdownItem
                          v-if="field.options?.length"
                          v-for="option in field.options"
                          :key="option.name"
                          :option="option"
                        />
                        <div v-else>
                          <div class="p-1.5 px-7 text-base text-gray-500">
                            {{ __('No {0} Available', [field.label]) }}
                          </div>
                        </div>
                      </div>
                      <div class="pt-1.5">
                        <Button
                          variant="ghost"
                          class="w-full !justify-start"
                          :label="__('Create New')"
                          @click="field.create()"
                        >
                          <template #prefix>
                            <FeatherIcon name="plus" class="h-4" />
                          </template>
                        </Button>
                      </div>
                    </div>
                  </template>
                </NestedPopover>
              </div>
              <DateTimePicker
                v-else-if="field.type === 'Datetime'"
                v-model="data[field.name]"
                :placeholder="__(field.placeholder || field.label)"
                input-class="border-none"
              />
              <DatePicker
                v-else-if="field.type === 'Date'"
                v-model="data[field.name]"
                :placeholder="__(field.placeholder || field.label)"
                input-class="border-none"
              />
              <FormControl
                v-else-if="
                  ['Small Text', 'Text', 'Long Text'].includes(field.type)
                "
                type="textarea"
                :placeholder="__(field.placeholder || field.label)"
                v-model="data[field.name]"
              />
              <FormControl
                v-else-if="['Int'].includes(field.type)"
                type="number"
                :placeholder="__(field.placeholder || field.label)"
                v-model="data[field.name]"
              />
              <FormControl
                v-else
                type="text"
                :placeholder="__(field.placeholder || field.label)"
                v-model="data[field.name]"
                :disabled="Boolean(field.read_only)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import NestedPopover from '@/components/NestedPopover.vue'
  import DropdownItem from '@/components/DropdownItem.vue'
  import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
  import UserAvatar from '@/components/UserAvatar.vue'
  import Link from '@/components/Controls/Link.vue'
  import { usersStore } from '@/stores/users'
  import { Tooltip, DatePicker, DateTimePicker, TextEditor } from 'frappe-ui'

  import { reactive, ref, watch, onMounted } from 'vue'
  
  const { getUser } = usersStore()
  
  const props = defineProps({
    sections: Array,
    data: Object,
  })

//   added for Desing Cpq 

const rangeErrors = reactive({})

const validateRangeIncrement = (name, value, min, max, step) => {

  const numericValue = parseFloat(value);
  const numericMin = parseFloat(min);
  const numericMax = parseFloat(max);
  const numericStep = parseFloat(step);

  if (!/^\d*\.?\d*$/.test(value)) {
     return 'Invalid Input.';
   }


   // Check if the value is outside the range
   if (numericValue < numericMin || numericValue > numericMax) {
     return `Value should be between ${min} and ${max}`;
   }

   // Extract the number of decimal places in the step
   const stepDecimalPlaces = step.toString().split('.')[1]?.length || 0;

   // Extract the number of decimal places in the value
   const valueDecimalPlaces = (value.toString().includes('.') ? value.split('.')[1].length : 0) || 0;

   if(stepDecimalPlaces > 0){
   // Check if the value has the correct number of decimal places as the step
   if (numericValue === numericMin || numericValue === numericMax) {
     return null; // No need for further validation
   }
   if (valueDecimalPlaces !== stepDecimalPlaces) {
     return `Value should increment by ${step}`;
   }
   }else {
     if (value.toString().includes('.') && value.toString().split('.')[1].length === 0) {
       return 'Invalid Input.'; // Error if there's a dot without succeeding digits
     }
     // If the step is an integer
     if ((numericValue - numericMin) % numericStep !== 0) {
       return `Value should increment by ${step}`;
     }
   }

   return null;
 };

 const updateRangeDisplay = (name, value) => {
   props.data[name] = value;
   const sizeElement = document.getElementById(name);
   if (sizeElement) {
     sizeElement.innerHTML = value;
   }
 };

 const handleRangeChange = (name, value, min, max, step) => {
   const errorMsg = validateRangeIncrement(name, value, min, max, step);
   rangeErrors[name] = errorMsg;
   props.data[name] = value;
 };

 const updateRangeValue = (name, value, min, max, step) => {
   const errorMsg = validateRangeIncrement(name, value, min, max, step);
   rangeErrors[name] = errorMsg;
   props.data[name] = value;
   const rangeElement = document.getElementsByClassName(name);
   if (rangeElement.length > 0) {
     rangeElement[0].value = value;
   }
 };

 const setInitialValues = () => {
   for (const section of props.sections) {
     for (const field of section.fields) {
       if (field.type === 'Range') {
         const name = field.name;
         const min = field.min;
         if (props.data[name] === undefined || props.data[name] === null || props.data[name] === '') {
           props.data[name] = min; // Set initial value to min if undefined, null, or empty string
           updateRangeValue(name, min, min, field.max, field.step);
           updateRangeDisplay(name, min);
         }
       }
     }
   }
 };

 onMounted(() => {
   watch(() => props.sections, (newValue, oldValue) => {
     if (newValue !== oldValue && newValue.length > 0) {
       setInitialValues();
     }
   })
 })
  </script>
  
  <style scoped>
  :deep(.form-control.prefix select) {
    padding-left: 2rem;
  }
  </style>
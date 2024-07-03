<template>
    <Dialog
      v-model="show"
      :options="{
        size: 'xl',
        actions: [
          {
            label: 'Close' ,
            variant: 'solid',
            
          },
        ],
      }"
    >
    <template #body-title>
        <h2 class="text-2xl font-bold leading-6 text-gray-900">{{__('Item Recommendation:')}}</h2>
      </template>
      <template #body-content>
        <div>
        <div v-if="!attributes || !Object.keys(attributes).length">
            <p class="text-gray-500">No valuable insights available.</p>
          </div>
          <div v-if="attributes && Object.keys(attributes).length">
            <h3 class="text-xl font-medium  text-gray-900 mt-6">{{__('Valuable Insights:')}}</h3><br/>
            <ul>
              <li v-for="(value, key) in attributes.attributes" :key="key" class="text-gray-500">
              <span class="text-gray-900">{{ key }}:</span> {{ value }}
            </li>
            </ul>
          </div>
           <h3 class="text-xl font-medium  text-gray-900 mt-6">{{__('Recommended Items:')}}'</h3><br/>
        
          <div v-if="!attributes || !attributes.items || !attributes.items.length">
            <p class="text-gray-500">{{__('No recommended items available.')}}'</p><br/>
            <div class="flex justify-center">
              <Button variant="solid" @click="createNewItem">{{__('Create Item')}}</Button>
            </div>
          </div>
          <div v-if="attributes && attributes.items && attributes.items.length">
            <ul>
             <li v-for="(item, index) in attributes.items" :key="index">
                {{ item.name }} - <span class="text-pink-700">{{ formatPrice(item.price) }}</span>
              </li>
          </ul>
          </div>
        </div>
      </template>
    </Dialog>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  // Define props to accept attributes and items
  const props = defineProps({
    attributes: Object,
    items: Array
  })
  
  // Function to format the price with commas
  function formatPrice(price) {
    if (price === 'Price not available') {
      return price
    }
    return 'Rs ' + parseFloat(price).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  }
  
  // Define any other necessary variables or functions here
  const show = ref(false)
  
  
  </script>
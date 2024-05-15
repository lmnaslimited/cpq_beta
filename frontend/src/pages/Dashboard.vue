<template>
  <div class="bg-gray-300">
    <!-- Layout Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>

    <div class="flex space-x-4 m-4">
      <!-- Grid occupying half of the screen width -->
      <div class="w-1/2">
        <div class="grid grid-cols-2 gap-4">
          <!-- Cards -->
          <!-- First card -->
          <div class="col-span-2 md:col-span-1 bg-white border border-gray-500 rounded-lg p-4 ">
            <h3 class="text-l text-black-300 mb-4 text-left">Opportunities Won (Current Month)</h3>
            <div style="font-size: 24px; color: gray; font-weight: bold; text-align: center;">251</div>
          </div>
          <!-- Second card -->
          <div class="col-span-2 md:col-span-1 bg-white border border-gray-500 rounded-lg p-4 ">
            <h3 class="text-l text-black-200 mb-4 text-left">Value of Own Opportunities (Current Month)</h3>
            <div style="font-size: 24px; color: gray; font-weight: bold; text-align: center;">$12,000</div>
          </div>
          <!-- Third card -->
          <div class="col-span-2 md:col-span-1 bg-white border border-gray-500 rounded-lg p-4 ">
            <h3 class="text-l text-black-200 mb-4 text-left">Leads (Current Month)</h3>
            <div style="font-size: 24px; color: gray; font-weight: bold; text-align: center;">252</div>
          </div>
          <!-- Fourth card -->
          <div class="col-span-2 md:col-span-1 bg-white border border-gray-500 rounded-lg p-4">
            <h3 class="text-l text-black-200 mb-4 text-left">Account Health Score (Current Month)</h3>
            <div style="font-size: 24px; color: gray; font-weight: bold; text-align: center;">4521</div>
          </div>
        </div>
      </div>
      <!-- Card occupying the other half of the screen width -->
      <div class="w-1/2">
        <div class="bg-white border border-gray-500 rounded-lg p-4 h-full">
          <h3 class="text-l mb-4">Top Rainmakers</h3>
          <div style="font-size: 16px;">
            <div class="grid grid-cols-4 gap-x-2">
              <div class="flex flex-col items-center">
                <img src="/image7.png" alt="Subashree" class="rounded-lg" style="max-width: 100px; height: auto;">
                <div class="mt-2">$234</div>
              </div>
              <div class="flex flex-col items-center">
                <img src="/image4.png" alt="Subashree" class="rounded-lg" style="max-width: 100px; height: auto;">
                <div class="mt-2">$200</div>
              </div>
              <div class="flex flex-col items-center">
                <img src="/image2.png" alt="Ayesha" class="rounded-lg" style="max-width: 100px; height: auto;">
                <div class="mt-2">$177</div>
              </div>
              <div class="flex flex-col items-center">
                <img src="/image3.png" alt="Eswari" class="rounded-lg" style="max-width: 100px; height: auto;">
                <div class="mt-2">$117</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Second row: 3 cards -->
    <div class="flex justify-between mt-2 ml-4 mr-4 mb-1">
      <!-- First card occupying 30% width -->
      <div class="w-1/3 mr-5">
        <div class="bg-white border border-gray-500 rounded-lg p-4 h-full">
          <h3 class="text-l text-black-200 mb-4">Value of Won Opportunities</h3>
          <h3 class="text-s text-black-200 mb-4">May 01, 2023 - May 01, 2024</h3>
          <div id="lineChart" class="chart"></div>
        </div>
      </div>

      <!-- Second card occupying 30% width -->
      <div class="w-1/3 mr-5">
        <div class="bg-white border border-gray-500 rounded-lg p-4 h-full">
          <h3 class="text-l text-black-200 mb-4">Accounts Subscribed</h3>
          <!-- <h3 class="text-m text-black-300 mb-4">Current Month</h3> -->
          <div id="doughnutChart" class="chart"></div>
        </div>
      </div>

      <!-- Third card occupying 40% width -->
      <div class="w-1/3">
        <div class="bg-white border border-gray-500 rounded-lg p-4 h-full">
          <h3 class="text-l text-black-300 mb-4">Accounts By Health score</h3>
          <div id="barChart" class="chart"></div>
        </div>
      </div>
    </div>

    <!-- Third row: 2 cards -->
    <div class="flex justify-between mt-4 ml-5 mr-5 mb-2">
      <div class="w-3/5">
        <div class="bg-white border border-gray-500 rounded-lg p-4 py-6 h-full"> 
    <h3 class="text-l text-black-500 mb-4">Opportunities</h3>
    <h3 class="text-m text-black-300 mb-4">current Month</h3>
    <!-- Grid layout for columns -->
    <div class="grid grid-cols-4 gap-3">
      <!-- Column 1: EMPLOYEE -->
      <div>
        <h4 class="text-lg mt-2">EMPLOYEE</h4> 
        <h4 class="text-l mt-5">subashree</h4>
        <p>Vinitha</p>
        <p>Ragavee</p>
      </div>
      <!-- Column 2: QUALIFIES -->
      <div>
        <h4 class="text-lg mt-2">QUALIFIES</h4>
        <h4 class="text-l mt-5">45</h4>
        <p>39</p>
        <p>20</p>
      </div>
      <!-- Column 3: WON -->
      <div>
        <h4 class="text-lg ">WON</h4>
        <h4 class="text-l mt-5">23</h4>
        <p>20</p>
        <p>19</p>
      </div>
      <!-- Column 4: VALUES -->
      <div>
        <h4 class="text-lg ">VALUES</h4>
        <h4 class="text-l mt-5">$277</h4>
        <p>$200</p>
        <p>$190</p>
      </div>
    </div>
  </div>
</div>

  <div class="w-1/2 ml-5">
    <div class="bg-white border border-gray-500 rounded-lg p-6 py-10 ">
      <h3 class="text-xl text-black-300 mb-4">Leads By Status</h3>
      <div id="pieChart" class="chart"></div>
    </div>
  </div>
</div>


  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs } from 'frappe-ui'
let title = 'Dashboard'
const breadcrumbs = [{ label: title, route: { name: 'Dashboard' } }]
import { onMounted } from 'vue';
import * as frappe from 'frappe-charts';

onMounted(() => {
  const barChartData = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [
      { name: 'Data 1', values: [12, 19, 3, 5, 2, 3] },
      { name: 'Data 2', values: [10, 15, 7, 9, 4, 6] }
    ]
  };

  const barChart = new frappe.Chart("#barChart", {
    data: barChartData,
    type: 'bar',
    height: 200, // Adjust the height here
     // Customize bar colors
  });

  const lineChartData = {
labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
datasets: [
{ name: 'Data 1', values: [10, 20, 15, 30, 25, 35] },
{ name: 'Data 2', values: [5, 15, 10, 25, 20, 30] }
]
};

const lineChart = new frappe.Chart("#lineChart", {
height : 160,
data: lineChartData,
type: 'line',
colors:['#F6A6BB', '#FE5D9F']
});

  const pieChartData = {
    labels: ['A', 'B', 'C', 'D'],
    datasets: [
      { name: 'Data', values: [30, 20, 10, 15] }
    ]
  };

  const pieChart = new frappe.Chart("#pieChart", {
    height: 160,
    data: pieChartData,
    type: 'pie' 
  });

  const doughnutChartData = {
    labels: ['Subscribed', 'Not Subscribed'],
    datasets: [
      { name: 'Data', values: [30, 20] }
    ]
  };

  const doughnutChart = new frappe.Chart("#doughnutChart", {
    height: 175,
    data: doughnutChartData,
    type: 'donut'
  });



});
</script>

<style scoped>
/* No specific styles added */
</style>

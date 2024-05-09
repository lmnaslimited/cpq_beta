<template>
  <div>
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
        <div class="col-span-2 md:col-span-1 ">
          <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 text-center">
            <h3 class="text-xl font-bold text-black-300 mb-4">Opportunities Won</h3>
            <div style="font-size: 24px; color: red; font-weight: bold ;">251</div>
          </div>
        </div>
        <!-- Second card -->
        <div class="col-span-2 md:col-span-1">
          <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 text-center">
            <h3 class="text-xl font-bold text-black-200 mb-4">Value of Own Opportunities</h3>
            <div style="font-size: 24px; color: green; font-weight: bold;">$12,000</div>
          </div>
        </div>
        <!-- Third card -->
        <div class="col-span-2 md:col-span-1">
          <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 text-center">
            <h3 class="text-xl font-bold text-black-300 mb-4">Leads</h3>
            <div style="font-size: 24px; color: green; font-weight: bold;">252</div>
          </div>
        </div>
        <!-- Fourth card -->
        <div class="col-span-2 md:col-span-1">
          <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 text-center">
            <h3 class="text-xl font-bold text-black-300 mb-4">Account Health Score</h3>
            <div style="font-size: 24px; color: red; font-weight: bold;">4521</div>
          </div>
        </div>
      </div>
    </div>
    <!-- Card occupying the other half of the screen width -->
    <div class="w-1/2">
  <div class="bg-gray-200 border border-gray-300 rounded-lg p-4 h-full">
    <h3 class="text-xl font-bold mb-4">Top Rainmakers</h3>
    <div style="font-size: 16px;">
      <div class="grid grid-cols-2 gap-x-4">
        <div>
          <div>Subashree</div>
          <div>Fathima</div>
          <div>Ayesha</div>
          <div>Eswari</div>
        </div>
        <div>
          <div>$234</div>
          <div>$200</div>
          <div>$177</div>
          <div>$117</div>
        </div>
      </div>
    </div>
  </div>
</div>


  </div>
    <!-- Second row: 3 cards -->
    <div class="flex justify-between mt-5 ml-5 mr-5">
    <!-- First card occupying 30% width -->
    <div class="w-1/3 mr-5">
      <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 h-full">
        <h3 class="text-xl font-bold mb-4">Card 1</h3>
        <div>Content 1</div>
      </div>
    </div>

    <!-- Second card occupying 30% width -->
    <div class="w-1/3 mr-5">
      <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 h-full">
        <h3 class="text-xl font-bold text-green-500 mb-4">Leads</h3>
        <div style="font-size: 48px; color: green; font-weight: bold;">842</div>
      </div>
    </div>

    <!-- Third card occupying 40% width -->
    <div class="w-1/3">
      <div class="bg-gray-200 border border-gray-400 rounded-lg p-4 h-full">
        <div id="barChart" class="chart" style="position: relative; top: 10px;"></div>
      </div>
    </div>
  </div>

    <!-- Third row: 2 cards -->
    <div class="flex justify-between mt-5 ml-5 mr-5">
      <div class="w-3/5">
        <div class="bg-gray-200 border border-gray-400 rounded-lg p-6 py-10">
          <div id="lineChart" class="chart"></div>
        </div>
      </div>
      <div class="w-1/2 ml-5">
        <div class="bg-gray-200 border border-gray-400 rounded-lg p-6 py-10">
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
    title: "Bar Chart",
    data: barChartData,
    type: 'bar',
    height: 170, // Adjust the height here
    colors: ['#ff0000', '#00ff00'] // Customize bar colors
  });

  const lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      { name: 'Data 1', values: [10, 20, 15, 30, 25, 35] },
      { name: 'Data 2', values: [5, 15, 10, 25, 20, 30] }
    ]
  };

  const lineChart = new frappe.Chart("#lineChart", {
    title: "Line Chart",
    data: lineChartData,
    type: 'line'
  });

  const pieChartData = {
    labels: ['A', 'B', 'C', 'D', 'E'],
    datasets: [
      { name: 'Data', values: [30, 20, 10, 15, 25] }
    ]
  };

  const pieChart = new frappe.Chart("#pieChart", {
    title: "Pie Chart",
    data: pieChartData,
    type: 'pie'
  });
});
</script>

<style scoped>
/* No specific styles added */
</style>

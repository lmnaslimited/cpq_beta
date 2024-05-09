<template>
    <div class="card">
    <div class="card-header">
    <h3 class="card-title">{{ title }}</h3>
    </div>
    <div class="card-body">
    <slot></slot>
    </div>
    </div>
    </template>
    
    <script>
    export default {
    props: {
    title: String
    }
    };
    </script>
    
    <style scoped>
    .card {
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    width: calc(50% - 10px); /* Set width of each card */
    margin-right: 15px; /* Adjust spacing between cards */
    float: left; /* Float cards to the left */
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center content vertically */
    }
    
    .card-header {
    padding: 10px;
    text-align: center; /* Center text horizontally */
    }
    
    .card-body {
    padding: 10px;
    text-align: center; /* Center text horizontally */
    }
    
    .card-title {
    margin: 0; /* Remove default margin */
    }
    </style>
    
    
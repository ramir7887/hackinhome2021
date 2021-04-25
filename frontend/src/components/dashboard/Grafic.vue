<template>
    <canvas ref="myChart" width="500" height="300"></canvas>
</template>

<script>
import Chart from 'chart.js';

export default {
  name: 'monthly-sales-chart',
  mounted() {
    new Chart(this.$refs.myChart, {
      type: 'pie',
      data: {
    datasets: [{
        data: [10, 20, 30],
        backgroundColor: [
            '#ff6384',
            '#36a2eb',
            '#cc65fe',
            '#ffce56'        ]
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: [
        'Red',
        'Yellow',
        'Blue'
    ]
}
    });
  }
}
</script>
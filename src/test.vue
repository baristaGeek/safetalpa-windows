<template>
  <div>
<!-- <button v-on:click='callPy'>Call py</button>
<button v-on:click='callPyy'>Call pyy</button> -->
<h2 style="text-align:center">SafeTalpa is protecting you</h2>
  </div>
</template>
<script>
var PythonShell = require('python-shell');
export default {
  name: 'test',
  // data () {
  //   return {
  //      days: 0,
  //      maliciousProcesses: 1
  //   }
  // },
  methods: {
    callPy () {
      PythonShell.run('./data-analysis/info_gathering.py', function (err) {});
    },
  },
  mounted() {
      setInterval(PythonShell.run('./data-analysis/info_gathering.py', function (err) {}),120000)
    }
  }
</script>

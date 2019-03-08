// ChartCreation

new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: [ 'UTA',  'DAL', 'CLE', 'SA', 'MEM', 'GS', 'ATL', 
      'BOS', 'DEN', 'MIN', 'SAC', 'PHO', 'WAS', 'OKC', 'CHI', 'IND', 
      'LAC', 'POR', 'DET', 'MIL', 'CHA', 'MIA', 'BKN', 'TOR', 'NO', 
      'NY', 'HOU', 'ORL', 'LAL', 'PHI'],
      datasets: [
        {
          label: "Points Allowed",
          backgroundColor: ["navy", "blue","maroon","silver","lightblue","gold", "red","green","powderblue", "black","purple","orange","blue","darkblue", "red","gold","blue", "red","blue","darkgreen","lightgreen","red", "black","grey","gold", "darkorange","darkred","blue","yellow","red"],
          data: [ 29.86, 30.01, 31.68, 28.2, 29.8, 31.21, 34.5, 33.89, 35.24, 31.51, 32.43, 35.42, 30.37, 
          32.35, 31.94, 32.55, 32.03, 33.96, 33.16, 29.11, 32.59, 30.29, 35.08, 30.96, 34.1, 30.68, 
          33.48, 33.72, 34.35, 32.36]

        }


      ]
    },
    options: {
    
    	title: {
         titleFontSize: 30,
        display: true,
        text: "",
      }
    }
});


// function f_getDoughnut(){
// var defaultURL = "/doughnut";
// d3.json(defaultURL,function(x) {
// console.log(x);
// console.log(x.value);
// })}

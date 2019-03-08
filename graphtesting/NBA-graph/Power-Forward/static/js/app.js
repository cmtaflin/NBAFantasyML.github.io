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
          data: [ 29.22, 28.26, 26.8, 27.98, 29.56, 31.18, 28.89, 32.42, 29.66, 30.02, 31.34, 32.67, 30.09, 31.7, 29.12, 32.33, 27.16, 31.68, 28.69, 27.82, 30.94, 27.51, 29.07, 29.05, 32.31, 31.6, 29.17, 28.86, 33.09, 29.09]

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

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
          data: [ 26.61, 27.72, 33.11, 31.36, 30.42, 32.12, 32.29, 28.64, 30.79, 27.31, 
          31.79, 29.65, 27.75, 28.54, 31.35, 31.42, 27.76, 28.06, 26.54, 25.24, 28.66, 
          28.11, 32.54, 27.08, 28.07, 31.25, 31.29, 29.57, 28.93, 30.56]

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

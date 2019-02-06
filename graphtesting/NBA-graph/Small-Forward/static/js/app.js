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
          label: "Fantasy Points Allowed",
          backgroundColor: ["navy", "blue","maroon","silver","lightblue","gold", "red","green","powderblue", "black","purple","orange","blue","darkblue", "red","gold","blue", "red","blue","darkgreen","lightgreen","red", "black","grey","gold", "darkorange","darkred","blue","yellow","red"],
          data: [ 26.22, 28.9, 29.98, 25.97, 28.54, 28.89, 31.21, 30.55, 31.4, 30.34, 
          33.01, 32.86, 30.56, 32.04, 29.1, 26.93, 32.74, 30.23, 30.01, 35.51, 32.42, 
          29.76, 33.2, 30.83, 32.84, 32.07, 32.39, 30.85, 32.31, 31.25]

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

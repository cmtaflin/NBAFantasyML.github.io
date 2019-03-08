// ChartCreation
//

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
          data: [ 23.52, 23.75, 24.02, 24.25, 24.79, 24.81, 24.99, 25.43, 25.53, 25.8, 25.83, 26.13, 26.41, 26.63, 26.77, 26.85, 26.97, 27.22, 27.27, 27.44, 27.6, 27.62, 28.29, 28.37, 28.48, 28.76, 29.05, 29.52, 30.53, 31.34]

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

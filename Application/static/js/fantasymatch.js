// Javascript file for the Fantasy matchup page - fantasymatch.html
function getSelectedValue(id) {
  var selectedValue = document.getElementById(id).value; 
  // console.log(this.target);
  d3.json(`/getids/${selectedValue}`).then(function (response) {
    // console.log(response);
    swal({
      text: "Applying Theatre Soda Layer...Please Wait!",
      showCloseButton: false,
      showCancelButton: false,
      showConfirmButton: false,
      allowOutsideClick: false
    })
    // console.log(response.Fantasy_Team_ID[0]);
    var teamId = response.Fantasy_Team_ID[0]
    d3.json(`/matchup_data/${teamId}/7110302003`).then(function (response1) {
      swal.close();
      team = response1.team1;
      Object.keys(team).map(function (data) {
        console.log(data);
        console.log(team[data]);
        var td = $('<td>').text(team[data]);
        if (id == 'list') {
          var tr = $('#team1');
          // tr.html('');
          tr.append(td);
        } else {
          var tr = $('#team2');
          // tr.html('');
          tr.append(td);
        }
      })
      // console.log(response1.team1);
    })
  })
}


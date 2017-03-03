$(document).ready(function() {
  var nature = []
  for(var i=1; i<=151;i++) {
    $('.dex').append(`<img id=\'img${i}\' src=\'/static/teambuilder/img/${i}.png\'>`);
  }
  natures = $.get(`http://pokeapi.co/api/v2/nature/`, function(data) {
    for (i in data.results) {
      $('#naturelist').append(`<option value='${data.results[i].name}'>${data.results[i].name}</option>`)
    }
  });
  morenatures = $.get(`http://pokeapi.co/api/v2/nature/?offset=20`, function(data) {
    for (i in data.results) {
      $('#naturelist').append(`<option value='${data.results[i].name}'>${data.results[i].name}</option>`)
    }

  });
  $('#save').click(function() {
    $('#statform').attr('save', 'true')
  });
  $('#calc').click(function() {
    $('#statform').attr('save', 'false')
  });
  $(document).on("click", "img", function() {
    pkmndata($(this).attr('id').substring(3))
    $('.stats #numname').text("Loading..")
    $("body").css("cursor", "progress");
    $('.stats #types').text("")
    $('#base_hp').html("<input type='hidden' name='hp_base' val=''>")
    $('#base_atk').html("<input type='hidden' name='atk_base' val=''>")
    $('#base_def').html("<input type='hidden' name='def_base' val=''>")
    $('#base_spa').html("<input type='hidden' name='spa_base' val=''>")
    $('#base_spd').html("<input type='hidden' name='spd_base' val=''>")
    $('#base_spe').html("<input type='hidden' name='spe_base' val=''>")
    console.log($(this).attr('id').substring(3))
    $('#id').val($(this).attr('id').substring(3))
    pkmn_info = $.get(`http://pokeapi.co/api/v1/pokemon/${$(this).attr('id').substring(3)}`, function(data) {
      $('.stats #numname').text(`#${data.pkdx_id} - ${data.name}`);
      $("body").css("cursor", "default");
      $('#base_hp').html(`${data.hp}<input type='hidden' name='hp_base' value=${data.hp}>`)
      $('#base_atk').html(`${data.attack}<input type='hidden' name='atk_base' value=${data.attack}>`)
      $('#base_def').html(`${data.defense}<input type='hidden' name='def_base' value=${data.defense}>`)
      $('#base_spa').html(`${data.sp_atk}<input type='hidden' name='spa_base' value=${data.sp_atk}>`)
      $('#base_spd').html(`${data.sp_def}<input type='hidden' name='spd_base' value=${data.sp_def}>`)
      $('#base_spe').html(`${data.speed}<input type='hidden' name='spe_base' value=${data.speed}>`)
      var type = data.types[0].name[0].toUpperCase() + data.types[0].name.substring(1);
      if(data.types.length > 1) {
        type = data.types[1].name[0].toUpperCase() + data.types[1].name.substring(1) + " " + type;
      }
      $('.stats #types').text(type);
    });
  });

  $('#statform').submit(function() {
    var formdata = $('#statform').serialize()
    if($('#statform').attr('save') == "true") {
      formdata+="&save=true";
    }
    console.log("Form Data:")
    console.log(formdata)
    $.ajax({
      url:"/teambuilder/stat_ajax/",
      method:"POST",
      success:function(obj) {
        if(obj.success) {
          // run the graph stuff
          $('.errors').html("");
          pkmndata(obj.pokemon[6], obj.pokemon);
        }
        else {
          errors_html = ""
          for(errors in obj.errors) {
            errors_html += `<li>${obj.errors[errors]}</li>`;
          }
          $('.errors').html(errors_html)
        }
      },
      data : formdata
    });
    console.log(formdata);
    return false;
  });
});

function pkmndata(num, obj){
    var url = "http://pokeapi.co/api/v1/pokemon/" + num + "/";
    var that = $.get(url, function(res) {
        var hp = res.hp;
        var attack = res.attack;
        var defense = res.defense;
        var spattack = res.sp_atk;
        var spdef = res.sp_def;
        var speed = res.speed;
        var name = res.name;
        var arr = [hp, attack, defense, spattack, spdef, speed, name];
        createChart(arr, obj);
    }, "json");
}

function createChart(arr, calc) {
  console.log("calc");
  console.log(calc);
  var data = [
    {"Criteria":"HP", "stat":100+2*arr[0],},
    {"Criteria":"Attack", "stat":5+2*arr[1],},
    {"Criteria":"Defense", "stat":5+2*arr[2],},
    {"Criteria":"Speed", "stat":5+2*arr[5],},
    {"Criteria":"Sp.Defense", "stat":5+2*arr[4],},
    {"Criteria":"Sp.Attack", "stat":5+2*arr[3],}
  ]
  if (calc != undefined) {
    $("#chart").kendoChart({
        title: {
            text: arr[6]
        },
        dataSource: data,
        seriesDefaults: {
            type: "radarArea",
        },
        series: [
          {
            name: "Base stats",
            data: [100+2*arr[0],5+2*arr[1],5+2*arr[2],5+2*arr[5],5+2*arr[4],5+2*arr[3]]
          },
          {
            name: "Calculated stats",
            data: [calc[0],calc[1],calc[2],calc[5],calc[4],calc[3]]
          },
        ],
        categoryAxis: {
            field: "Criteria"
        },
        valueAxis: {
          max: 500
        },
        tooltip: {
            visible: true,
            format: "{0}"
        },
        theme: "Fiori"
    });
  } else {
    $("#chart").kendoChart({
        title: {
            text: arr[6]
        },
        dataSource: data,
        seriesDefaults: {
            type: "radarArea",
            // style: ""
        },
        series: [
          {
            name: "Base stats",
            data: [100+2*arr[0],5+2*arr[1],5+2*arr[2],5+2*arr[5],5+2*arr[4],5+2*arr[3]]
          },
        ],
        categoryAxis: {
            field: "Criteria"
        },
        valueAxis: {
          max: 500
        },
        tooltip: {
            visible: true,
            format: "{0}"
        },
        theme: "Fiori"
    });
  }
}
$(document).bind("kendo:skinChange", createChart);

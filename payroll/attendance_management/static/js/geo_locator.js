function geoFindMe() {

  const status = document.querySelector('#status');

  function success(position) {
    const latitude  = position.coords.latitude;
    const longitude = position.coords.longitude;

    status.textContent = '';
    employee_name = window.location.href.split("/")[5]
    window.location.href=`/attendance/employee_check_in/${employee_name}`;
  }

  function error(err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
      employee_name = window.location.href.split("/")[5]
      window.location.href=`/attendance/employee_check_in/${employee_name}`;
  }

  if (!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  }else{
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }

}

window.onload = geoFindMe();

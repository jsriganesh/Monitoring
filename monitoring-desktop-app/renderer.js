const { exec } = require('child_process');

const path = require('path');
const SYSTEMINFO_STORAGE_KEY = 'SYSTEM_INFO'



const sysInfoScriptPath = path.join(__dirname, './script/get-sys-info.py');

const getDownloadAndUploadSpeed= async()=>{
    const sysInfo = await exec(`python3 ${sysInfoScriptPath}`, (error, stdout, stderr) => {
      if (error) {
          console.error(`Error: ${error.message}`);
          return;
      }
      if (stderr) {
          console.error(`stderr: ${stderr}`);
          return;
      }
      const correctedJsonString = stdout.replace(/'/g, '"');

      console.log('stdout:--- $',correctedJsonString);
      console.log('stdout:--- $',JSON.parse(correctedJsonString));
      const parseDate = JSON.parse(correctedJsonString)
      console.log('upload:--- $',parseDate);
      setTheDatainLocal(parseDate)
    })

    sysInfo.on('exit', (code) => {
      if (code === 403) {
          console.error('HTTP Error 403: Forbidden');
      }
  });
}

const setTheDatainLocal=(value)=>{
  
  const getAllInfo =   localStorage.getItem(SYSTEMINFO_STORAGE_KEY);
  console.log('getAllInfo  ===> ',getAllInfo)
  // if(getAllInfo) {
    const list = getAllInfo ?  JSON.parse(getAllInfo) :{}
    console.log('list  ===> ',list)
    console.log('value  ===> ',value)
    if (list[value.date]) {
      // If it exists, merge the new value with the existing list
      list[value.date] = [...list[value.date], value];
    } else {
      // If it doesn't exist, initialize a new list with the new value
      list[value.date] = [value];
    }
    // list['value.date'] = [...list[value.date],...value]
  // }
  
  localStorage.setItem(SYSTEMINFO_STORAGE_KEY, JSON.stringify(list));

  setTimeout(()=>{
    getDownloadAndUploadSpeed()
  },300000)

}

  console.log(getDownloadAndUploadSpeed())

// para peticiones get con axios
async function getRequest(url, params = {}) {
    try {
      const res = await axios.get(url, { params });
      if (res.success){
        return res
      }
    } catch (error) {
      console.error("Error en la petición GET:", error);
    }
  }

  
  // para peticiones post con axios
  async function postRequest(url, data) {
    try {
      const res = await axios.post(url, data);

      if (res.status == 200){
        return res.data
      }
    } catch (error) {
      console.error("Error en la petición POST:", error);
    }
  }
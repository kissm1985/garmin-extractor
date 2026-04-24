const DEFAULT_API = "";

function getApiBase() {
  return localStorage.getItem("apiBase") || DEFAULT_API;
}

function setApiBase(url) {
  localStorage.setItem("apiBase", url);
}

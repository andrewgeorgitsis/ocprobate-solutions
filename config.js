// Contact-form endpoint. Posts JSON to the in-house /api/lead serverless function,
// which files the lead in the Lead To Close CRM (tagged `probate`, assigned to Vennessa).
window.SITE_CONFIG = { formEndpoint: "/api/lead" };

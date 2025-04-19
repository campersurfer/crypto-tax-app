import React from "react";

const Disclaimer: React.FC = () => (
  <div className="max-w-2xl mx-auto my-16 p-8 bg-base-200 rounded shadow">
    <h1 className="text-3xl font-bold mb-4 text-warning">Legal Disclaimer</h1>
    <p className="mb-4 text-base-content">
      This application and its AI-powered features are provided for informational purposes only and do not constitute legal, tax, or financial advice. Users should consult a qualified tax professional or legal advisor for guidance specific to their situation. The app's outputs, including all AI-generated summaries and classifications, are not guaranteed to be accurate or sufficient for compliance purposes.
    </p>
    <p className="text-sm text-base-content opacity-70">
      By using this app, you acknowledge and accept that all information is provided "as is" without warranty of any kind, and you assume full responsibility for any actions taken based on the app's outputs.
    </p>
  </div>
);

export default Disclaimer;

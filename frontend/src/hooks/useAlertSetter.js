import { useState } from "react";

function useAlertSetter() {
    const [alert, setAlert] = useState({
        visible: false,
        severity: "",
        message: "",
    });

    const showAlert = (severity, message) => {
        setAlert({ visible: true, severity: severity, message: message });
        hideAlert();
    };

    const hideAlert = () => {
        setTimeout(() => {
            setAlert({ visible: false, severity: "", message: "" });

          }, 3000);
    };

    return { alert, showAlert, hideAlert };
}

export default useAlertSetter;
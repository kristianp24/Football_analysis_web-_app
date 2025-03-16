import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = ({ element: Element, ...rest }) => {
    const token = localStorage.getItem("token");

    if (!token) {
        return <Navigate to="/" replace />;
    }

    return <Element {...rest} />;
};


export default ProtectedRoute;

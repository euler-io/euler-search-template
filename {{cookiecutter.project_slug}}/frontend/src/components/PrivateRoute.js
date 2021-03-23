import React from "react";
import PropTypes from "prop-types";
import AuthService from "./auth";
import { Redirect, Route, useLocation } from "react-router-dom";
import qs from "querystring";

const PrivateRoute = ({ component: Component, auth, children, ...rest }) => {
  const location = useLocation();
  if (auth.isLoggedIn()) {
    return <Component {...rest}>{children}</Component>;
  } else {
    let next = location.pathname;
    if (location.search) {
      next = `${location.pathname}${location.search}`;
    }
    const state = { referrer: next };
    const search = `?${qs.stringify({ next })}`;
    const to = {
      pathname: auth.params.loginURL,
      search: search,
      state: state,
    };
    return <Redirect to={to} />;
  }
};

PrivateRoute.propTypes = {
  component: PropTypes.elementType,
  auth: PropTypes.objectOf(AuthService).isRequired,
};

PrivateRoute.defaultProps = {
  component: Route,
};

export default PrivateRoute;
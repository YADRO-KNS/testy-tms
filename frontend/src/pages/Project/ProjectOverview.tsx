import React, {useContext, useEffect} from "react";
import {ProjectActiveTabContext} from "./ProjectMain";

const ProjectOverview = () => {
  const {setProjectActiveTab} = useContext(ProjectActiveTabContext)
  useEffect(() => {
    setProjectActiveTab('overview')
  }, [])

  return (
      <p>Project Overview</p>
  )
}

export default ProjectOverview
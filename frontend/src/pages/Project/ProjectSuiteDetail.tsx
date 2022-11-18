import React from "react";
import {useGetSuiteQuery} from "../../features/suite/suiteApi";
import ContainerLoader from "../../components/Loader/ContainerLoader";

interface ProjectSuiteDetailProps {
  suiteId: string
}

const ProjectSuiteDetail = ({suiteId} : ProjectSuiteDetailProps) => {
  const {data: suite, isLoading} = useGetSuiteQuery(suiteId)

  if (isLoading) return <ContainerLoader/>

  return (
      <p>

      </p>
  )
}

export default ProjectSuiteDetail
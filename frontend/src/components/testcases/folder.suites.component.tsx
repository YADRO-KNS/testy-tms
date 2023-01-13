import Typography from '@mui/material/Typography';
import React, {useEffect, useState} from "react";
import {treeSuite} from "./suites.component";
import TreeView from "@mui/lab/TreeView";
import TreeItem, {TreeItemContentProps, useTreeItem} from "@mui/lab/TreeItem";
import SvgIcon from "@mui/material/SvgIcon";
import IconButton from "@mui/material/IconButton";
import TextField from "@mui/material/TextField";
import {alpha, styled} from '@mui/material/styles';
import {TreeItemProps} from '@mui/lab/TreeItem';
import clsx from 'clsx';
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';

function MinusSquare() {
    return (
        <SvgIcon fontSize="inherit" style={{width: 14, height: 14}}>
            {/* tslint:disable-next-line: max-line-length */}
            <path
                d="M22.047 22.074v0 0-20.147 0h-20.12v0 20.147 0h20.12zM22.047 24h-20.12q-.803 0-1.365-.562t-.562-1.365v-20.147q0-.776.562-1.351t1.365-.575h20.147q.776 0 1.351.575t.575 1.351v20.147q0 .803-.575 1.365t-1.378.562v0zM17.873 11.023h-11.826q-.375 0-.669.281t-.294.682v0q0 .401.294 .682t.669.281h11.826q.375 0 .669-.281t.294-.682v0q0-.401-.294-.682t-.669-.281z"/>
        </SvgIcon>
    );
}

function PlusSquare() {
    return (
        <SvgIcon fontSize="inherit" style={{width: 14, height: 14}}>
            {/* tslint:disable-next-line: max-line-length */}
            <path
                d="M22.047 22.074v0 0-20.147 0h-20.12v0 20.147 0h20.12zM22.047 24h-20.12q-.803 0-1.365-.562t-.562-1.365v-20.147q0-.776.562-1.351t1.365-.575h20.147q.776 0 1.351.575t.575 1.351v20.147q0 .803-.575 1.365t-1.378.562v0zM17.873 12.977h-4.923v4.896q0 .401-.281.682t-.682.281v0q-.375 0-.669-.281t-.294-.682v-4.896h-4.923q-.401 0-.682-.294t-.281-.669v0q0-.401.281-.682t.682-.281h4.923v-4.896q0-.401.294-.682t.669-.281v0q.401 0 .682.281t.281.682v4.896h4.923q.401 0 .682.281t.281.682v0q0 .375-.281.669t-.682.294z"/>
        </SvgIcon>
    );
}

function CloseSquare() {
    return (
        <SvgIcon
            className="close"
            fontSize="inherit"
            style={{width: 14, height: 14, justifyContent: "start"}}
        >
            {/* tslint:disable-next-line: max-line-length */}
            <path
                d="M17.485 17.512q-.281.281-.682.281t-.696-.268l-4.12-4.147-4.12 4.147q-.294.268-.696.268t-.682-.281-.281-.682.294-.669l4.12-4.147-4.12-4.147q-.294-.268-.294-.669t.281-.682.682-.281.696 .268l4.12 4.147 4.12-4.147q.294-.268.696-.268t.682.281 .281.669-.294.682l-4.12 4.147 4.12 4.147q.294.268 .294.669t-.281.682zM22.047 22.074v0 0-20.147 0h-20.12v0 20.147 0h20.12zM22.047 24h-20.12q-.803 0-1.365-.562t-.562-1.365v-20.147q0-.776.562-1.351t1.365-.575h20.147q.776 0 1.351.575t.575 1.351v20.147q0 .803-.575 1.365t-1.378.562v0z"/>
        </SvgIcon>
    );
}

const CustomContent = React.forwardRef(function CustomContent(
    props: TreeItemContentProps,
    ref,
) {
    const {
        classes,
        className,
        label,
        nodeId,
        icon: iconProp,
        expansionIcon,
        displayIcon,
    } = props;

    const {
        disabled,
        expanded,
        selected,
        focused,
        handleExpansion,
        handleSelection,
        preventSelection,
    } = useTreeItem(nodeId);

    const icon = iconProp || expansionIcon || displayIcon;

    const handleMouseDown = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        preventSelection(event);
    };
    const handleExpansionClick = (
        event: React.MouseEvent<HTMLDivElement, MouseEvent>,
    ) => {
        handleExpansion(event);
    };

    const handleSelectionClick = (
        event: React.MouseEvent<HTMLDivElement, MouseEvent>
    ) => {
        handleSelection(event);
        document.getElementById(nodeId)?.scrollIntoView();
    };
    return (
        <div
            id={nodeId + "Folder"}
            className={clsx(className, classes.root, {
                [classes.expanded]: expanded,
                [classes.selected]: selected,
                [classes.focused]: focused,
                [classes.disabled]: disabled,
            })}
            style={{width: "max-content"}}
            onMouseDown={handleMouseDown}
            ref={ref as React.Ref<HTMLDivElement>}
        >
            <div onClick={handleExpansionClick} className={classes.iconContainer}>
                {icon}
            </div>
            <Typography
                onClick={(e) => handleSelectionClick(e)}
                component="div"
                sx={{fontSize: 15}}
            >
                {label}
            </Typography>
        </div>
    );
});


const StyledTreeItem = styled((props: TreeItemProps) => (
    <TreeItem ContentComponent={CustomContent} {...props}/>
))(({theme}) => ({
    "& .MuiTreeItem-iconContainer": {
        '& .close': {
            opacity: 0.3,
        },
    },
    "& .MuiTreeItem-group": {
        marginLeft: 15,
        paddingLeft: 2,
        borderLeft: `1px dashed ${alpha(theme.palette.text.primary, 0.4)}`,
    },
    "& .MuiTreeItem-root": {
        marginTop: 3,
        marginBottom: 3,
    },
}));

const Suite = (props: {
    row: treeSuite, nodeId: number
}) => {
    const {row} = props;
    return (
        <StyledTreeItem
            ContentComponent={CustomContent} label={row.name} nodeId={row.id.toString()}>
            {row.children.map((suite: any) => (
                <Suite key={suite.id} row={suite} nodeId={suite.id}
                />
            ))}
        </StyledTreeItem>
    );
}

const FolderSuites = (props: {
    selectedSuiteForTreeView: treeSuite | undefined
}) => {
    const {selectedSuiteForTreeView} = props;
    const [expanded, setExpanded] = useState<string[]>([])
    const [selected, setSelected] = useState<string[]>([])
    const [currentSuiteNumber, setCurrentSuiteNumber] = useState<number>(0)
    const [totalSuitesNumber, setTotalSuitesNumber] = useState<number>(0)
    const [suitesHtmlElmArrayLocal, setSuitesHtmlElmArrayLocal] = useState<any[]>([])
    const [hover, setHover] = useState<any>(null)

    const handleToggle = (event: React.SyntheticEvent, nodeIds: string[]) => {
        setExpanded(nodeIds);
    };

    useEffect(() => {
        const suitesIdArray: string[] = []
        if (selectedSuiteForTreeView) {
            const fillExpandedSuite = (childrenSuitesArr: treeSuite[]) => {
                childrenSuitesArr.map((suite) => {
                    if (suite.children.length > 0) {
                        fillExpandedSuite(suite.children)
                    }
                    suitesIdArray.push(suite.id.toString())
                })
            }
            suitesIdArray.push(selectedSuiteForTreeView.id.toString())
            fillExpandedSuite(selectedSuiteForTreeView.children)
        }
        setExpanded(suitesIdArray)
    }, [selectedSuiteForTreeView]);

    const onChangeName = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        if (e.target.value && selectedSuiteForTreeView) {
            const query = e.target.value.toLowerCase()
            const foundSuites: treeSuite[] = []
            const findSuitesByName = (childrenSuitesArr: treeSuite[]) => {
                childrenSuitesArr.map((suite) => {
                    if (suite.name.toLowerCase().includes(query)) {
                        foundSuites.push(suite)
                    }
                    if (suite.children.length > 0) {
                        findSuitesByName(suite.children)
                    }
                })
            }
            if (selectedSuiteForTreeView.name.toLowerCase().includes(query)) {
                foundSuites.push(selectedSuiteForTreeView)
            }
            findSuitesByName(selectedSuiteForTreeView.children)
            const suitesIdArray: string[] = []
            let suitesHtmlElmArray: any[] = []

            foundSuites.map((suite) => {
                const foundElement = document.getElementById(suite.id.toString() + "Folder")
                if (foundElement) {
                    suitesIdArray.push(suite.id.toString())
                    suitesHtmlElmArray.push(document.getElementById(suite.id.toString() + "Folder"))
                }
            })

            suitesHtmlElmArray.sort(function (elm1, elm2) {
                const elm1Y = elm1.getBoundingClientRect().y
                const elm2Y = elm2.getBoundingClientRect().y
                if (elm1Y < elm2Y) {
                    return -1
                }
                if (elm1Y > elm2Y) {
                    return 1
                }
                return 0
            })
            if (suitesHtmlElmArray.length > 0) {
                setCurrentSuiteNumber(1)
                setTotalSuitesNumber(suitesHtmlElmArray.length)
                suitesHtmlElmArray[0].scrollIntoView({block: "center", inline: "nearest"})
                if (hover) {
                    hover.style.backgroundColor = ""
                }
                suitesHtmlElmArray[0].style.backgroundColor = '#a6c4e5'
                setHover(suitesHtmlElmArray[0])
                setSuitesHtmlElmArrayLocal(suitesHtmlElmArray)
            } else {
                if (hover) {
                    hover.style.backgroundColor = ""
                }
                setHover(null)
                setCurrentSuiteNumber(0)
                setTotalSuitesNumber(0)
            }
            setSelected(suitesIdArray)
        } else {
            if (hover) {
                hover.style.backgroundColor = ""
            }
            setHover(null)
            setCurrentSuiteNumber(0)
            setTotalSuitesNumber(0)
            setSelected([])
        }
    }

    const nextSuite = () => {
        if (currentSuiteNumber != totalSuitesNumber) {
            if (suitesHtmlElmArrayLocal[currentSuiteNumber].getBoundingClientRect().bottom > window.innerHeight) {
                suitesHtmlElmArrayLocal[currentSuiteNumber].scrollIntoView({
                    block: "center",
                    inline: "nearest"
                })
            } else {
                suitesHtmlElmArrayLocal[currentSuiteNumber].scrollIntoView({
                    block: "nearest",
                    inline: "nearest"
                })
            }
            hover.style.backgroundColor = ""
            suitesHtmlElmArrayLocal[currentSuiteNumber].style.backgroundColor = '#a6c4e5'
            setHover(suitesHtmlElmArrayLocal[currentSuiteNumber])
            setCurrentSuiteNumber((prevState => prevState + 1))
        } else {
            suitesHtmlElmArrayLocal[0].scrollIntoView({
                block: "nearest",
                inline: "nearest"
            })
            hover.style.backgroundColor = ""
            suitesHtmlElmArrayLocal[0].style.backgroundColor = '#a6c4e5'
            setHover(suitesHtmlElmArrayLocal[0])
            setCurrentSuiteNumber(1)
        }
    }

    const prevSuite = () => {
        if (currentSuiteNumber - 2 >= 0) {
            suitesHtmlElmArrayLocal[currentSuiteNumber - 2].scrollIntoView({
                block: "nearest",
                inline: "nearest"
            })
            hover.style.backgroundColor = ""
            suitesHtmlElmArrayLocal[currentSuiteNumber - 2].style.backgroundColor = '#a6c4e5'
            setHover(suitesHtmlElmArrayLocal[currentSuiteNumber - 2])
            setCurrentSuiteNumber((prevState => prevState - 1))
        } else {
            suitesHtmlElmArrayLocal[totalSuitesNumber - 1].scrollIntoView({
                block: "nearest",
                inline: "nearest"
            })
            hover.style.backgroundColor = ""
            suitesHtmlElmArrayLocal[totalSuitesNumber - 1].style.backgroundColor = '#a6c4e5'
            setHover(suitesHtmlElmArrayLocal[totalSuitesNumber - 1])
            setCurrentSuiteNumber(totalSuitesNumber)
        }
    }

    return (

        <div style={{
            height: "100%"
        }}>
            {selectedSuiteForTreeView !== undefined &&
            <div style={{
                height: "100%"
            }}>
                <div style={{
                    height: "15%",
                    minHeight: "max-content",
                    margin: "15px 0px 0px 20px",
                }}>
                    <div>
                        <TextField
                            onChange={(content) => onChangeName(content)}
                            autoComplete="off"
                            style={{width: "95%"}}
                            placeholder="Поиск..."
                            variant={"outlined"}
                        />
                    </div>

                    {currentSuiteNumber != 0 &&
                    <div style={{display: "flex", flexDirection: "row", width: "100%", height: "35%", marginTop: 7}}>
                        <IconButton style={{width: "8%", height: "100%"}} onClick={() => prevSuite()}>
                            <KeyboardArrowLeftIcon/>
                        </IconButton>
                        <div style={{height: "100%"}}>{currentSuiteNumber} / {totalSuitesNumber}</div>
                        <IconButton style={{width: "8%", height: "100%"}} onClick={() => nextSuite()}>
                            <KeyboardArrowRightIcon/>
                        </IconButton>
                    </div>}
                </div>
                <div style={{
                    backgroundColor: "white", borderRadius: 10, margin: "13px 13px 13px 13px ",
                    height: "100%", overflowY: "auto", overflowX: "auto"
                }}>
                    <TreeView
                        aria-label="customized"
                        expanded={expanded}
                        selected={selected}
                        defaultCollapseIcon={<MinusSquare/>}
                        defaultExpandIcon={<PlusSquare/>}
                        defaultEndIcon={<CloseSquare/>}
                        onNodeToggle={handleToggle}
                        sx={{
                            flexGrow: 1,
                            margin: 1,
                            textAlign: "left",
                        }}
                    >
                        <Suite key={selectedSuiteForTreeView.id} row={selectedSuiteForTreeView}
                               nodeId={selectedSuiteForTreeView.id}
                        />
                    </TreeView>
                </div>
            </div>}
        </div>
    );
}
export default FolderSuites
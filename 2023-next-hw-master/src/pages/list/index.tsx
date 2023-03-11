import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { DELETE_SUCCESS, DELETE_USER_BOARD_SUCCESS, FAILURE_PREFIX } from "../../constants/string";
import { request } from "../../utils/network";
import { BoardMetaData } from "../../utils/types";

interface ListScreenProps {
    userName?: string;
}

const ListScreen = (props: ListScreenProps) => {
    /**
     * @todo [Step 5] 请在下述一处代码缺失部分填写合适的代码，完成游戏记录列表页面 UI
     * @todo [Step 6] 请在下述两处代码缺失部分填写合适的代码，完成网络请求的管理
     */
    const [refreshing, setRefreshing] = useState<boolean>(true);
    const [boardList, setBoardList] = useState<BoardMetaData[]>([]);

    const router = useRouter();
    const query = router.query;

    useEffect(() => {
        if (!router.isReady) {
            return;
        }

        fetchList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [router, query]);

    const fetchList = () => {
        setRefreshing(true);
        request(props.userName ? `/api/user/${props.userName}` : "/api/boards", "GET")
            .then((res) => {
                setBoardList(res.boards.map((val: any) => ({ ...val, name: val.boardName })));
                setRefreshing(false);
            })
            .catch((err) => {
                alert(FAILURE_PREFIX + err);
                setRefreshing(false);
            });
    };
    const deleteBoard = (id: number) => {
        // Step 6 BEGIN

        // Step 6 END
    };
    const deleteUserBoard = () => {
        // Step 6 BEGIN

        // Step 6 END
    };

    return refreshing ? (
        <p> Loading... </p>
    ) : (
        <div style={{ padding: 12 }}>
            {props.userName ? (
                <h4> Boards of {props.userName} </h4>
            ) : null}
            <button onClick={() => router.push("/")}>
                Go back to free mode
            </button>
            {props.userName ? (
                <button onClick={() => router.push("/list")}>
                    Go to full list
                </button>
            ) : null}
            {props.userName ? (
                <button onClick={deleteUserBoard}>
                    Delete all boards of this user
                </button>
            ) : null}
            {boardList.length === 0 ? (
                <p> Empty list. </p>
            ) : (
                <div style={{ display: "flex", flexDirection: "column" }}>{
                    // Step 5 BEGIN

                    // Step 5 END
                }</div>
            )}
        </div>
    );
};

export default ListScreen;
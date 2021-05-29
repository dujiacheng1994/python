#include <stdlib.h>
#include <stack>
#include <vector>
#include <stdio.h>
using namespace std;
struct TreeNode
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

vector<int> postorderTraversal(TreeNode* root)
{
    stack<TreeNode*> mystack;
    vector<int> ans;
    TreeNode* curr = root;
    TreeNode* pre = NULL;
    while(curr || !mystack.empty())
    {
        while(curr)
        {
            mystack.push(curr);
            curr = curr->left;
        }
        curr = mystack.top();

        //���ҽڵ��Ѿ����ʹ�����û���ҽڵ�  ������ýڵ�ֵ
        if(!curr->right || pre == curr->right)
        {
            mystack.pop();
            //ans.push_back(curr->val);
            printf("%d ",curr->val);
            pre = curr;
            curr = NULL;
        }
        else
        {
            curr = curr->right;
            pre = NULL;
        }
    }
    return ans;
}
int main(){
    TreeNode *root = new TreeNode(0);
    root->left = new TreeNode(1);
    root->right = new TreeNode(2);
    postorderTraversal(root);
    return 0;
}

